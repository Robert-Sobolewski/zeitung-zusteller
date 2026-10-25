package com.zeitungszusteller.app.domain.entity;

import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name="zustellers")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Zusteller {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	/**
	 * Zustellers first name
	 */
	@Column(name = "first_name", nullable = false)
	private String firstName;
	
	/**
	 * Zustellers last name
	 */
	@Column(unique = false, nullable = false)
	private String lastName;
	
	/**
	 * User role one of ADMIN, MANAGER, ZUSTELLER
	 */
	@Column(unique = false, nullable = false, length = 20)
	@JdbcTypeCode(SqlTypes.NAMED_ENUM)
	@Enumerated(EnumType.STRING)
	private UserRole role = UserRole.ZUSTELLER;

}
