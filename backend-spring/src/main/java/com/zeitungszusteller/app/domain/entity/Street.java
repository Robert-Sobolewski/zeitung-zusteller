package com.zeitungszusteller.app.domain.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name="streets")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Street {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	/** FK → bezirke.id (column is bezirk_id in the schema) */
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "bezirk_id", nullable = false)
	private Bezirk bezirk;
	
	@Column(nullable = false, unique = false)
	private String name;
	
	private int route_order;
}
