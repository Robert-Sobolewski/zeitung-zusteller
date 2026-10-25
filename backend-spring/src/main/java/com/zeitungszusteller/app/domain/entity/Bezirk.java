package com.zeitungszusteller.app.domain.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


/**
 * Represents districts
 */
@Entity
@Table(name="bezirke")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Bezirk {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	/**
	 * bezirk code , ex: 8019
	 */
	@Column(nullable = false, unique = true)
	private String code;
	
	/**
	 * describe bezirke location
	 */
	@Column(nullable=false, unique =false)
	private String name;
	
	/**
	 * FK → zustellers.id. One zusteller delivers many bezirke,
	 * so from THIS side (bezirk) it is a ManyToOne.
	 */
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "zusteller_id", nullable = false)
	private Zusteller zusteller;

}
