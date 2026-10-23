package com.zeitungszusteller.app;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase;
import org.springframework.boot.testcontainers.context.ImportTestcontainers;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.utility.DockerImageName;

import javax.sql.DataSource;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Harness smoke test — proves the whole test pipeline works:
 * 1. Testcontainers starts a disposable PostGIS container (same image as docker-compose),
 * 2. db/init/*.sql loads the full application schema into it,
 * 3. all 7 tables exist and are queryable.
 *
 * Every JPA/repository test in this project copies the container pattern below.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@ImportTestcontainers // 1. Włączamy automatyczne zarządzanie cyklem życia kontenerów przez JUnit 5
class SchemaSmokeTest {

    @Autowired
    private DataSource dataSource;

    // 2. Zamieniamy @Bean na @Container. Pole musi być 'public static final'
    @Container
    @ServiceConnection
    public static final PostgreSQLContainer<?> postgres = 
        new PostgreSQLContainer<>(
        		DockerImageName.parse("postgis/postgis:16-3.4")
        		.asCompatibleSubstituteFor("postgres"));
        

    @Test
    void schemaFromDbInitIsLoaded() throws Exception {
        String sql = """
            SELECT count(*) FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name IN ('zustellers', 'bezirke', 'streets', 'delivery_points',
                                 'newspaper_types', 'subscriptions', 'sync_outbox')
            """;
        try (var conn = dataSource.getConnection();
             var rs = conn.createStatement().executeQuery(sql)) {
            rs.next();
            assertThat(rs.getInt(1)).as("tables from 02-schema.sql").isEqualTo(7);
        }
    }
}
