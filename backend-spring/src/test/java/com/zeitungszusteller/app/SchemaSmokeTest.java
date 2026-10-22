package com.zeitungszusteller.app;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Bean;
import org.testcontainers.containers.PostgreSQLContainer;

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
class SchemaSmokeTest {

    @Autowired
    private DataSource dataSource;

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

    /** Disposable PostGIS container — same image as the production compose stack. */
    @ServiceConnection
    @Bean
    static PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>("postgis/postgis:16-3.4");
    }
}
