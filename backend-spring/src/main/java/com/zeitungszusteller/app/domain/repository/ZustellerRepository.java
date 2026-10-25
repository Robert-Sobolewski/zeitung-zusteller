package com.zeitungszusteller.app.domain.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.zeitungszusteller.app.domain.entity.UserRole;
import com.zeitungszusteller.app.domain.entity.Zusteller;

public interface ZustellerRepository extends JpaRepository<Zusteller, Long> {
	List<Zusteller> findByRole(UserRole role);
}
