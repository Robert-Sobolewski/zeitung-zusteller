package com.zeitungszusteller.app.domain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase;
import org.springframework.boot.testcontainers.context.ImportTestcontainers;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.utility.DockerImageName;

import com.zeitungszusteller.app.domain.entity.UserRole;
import com.zeitungszusteller.app.domain.entity.Zusteller;
import com.zeitungszusteller.app.domain.repository.ZustellerRepository;


@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@ImportTestcontainers
class ZustellerRepositoryTest {
	
	@Autowired
	private ZustellerRepository repository;
	
	@Container
	@ServiceConnection
	public static final PostgreSQLContainer<?> postgres = 
			new PostgreSQLContainer<>(
					DockerImageName.parse("postgis/postgis:16-3.4")
					.asCompatibleSubstituteFor("postgres")
					);

	
	
	@Test
	void findByRoleReturnsOnlyMatchingZusteller() {
		Zusteller roberto = new Zusteller();
		roberto.setFirstName("Roberto");
		roberto.setLastName("Sobolewski");
		roberto.setRole(UserRole.ZUSTELLER);

		Zusteller admin = new Zusteller();
		admin.setFirstName("Anna");
		admin.setLastName("Admin");
		admin.setRole(UserRole.ADMIN);

		repository.saveAll(List.of(roberto, admin));

		List<Zusteller> zustellerOnly = repository.findByRole(UserRole.ZUSTELLER);

		assertEquals(1, zustellerOnly.size());
		assertEquals("Roberto", zustellerOnly.get(0).getFirstName());
		assertTrue(repository.findAll().size() >= 2);
	}
}
