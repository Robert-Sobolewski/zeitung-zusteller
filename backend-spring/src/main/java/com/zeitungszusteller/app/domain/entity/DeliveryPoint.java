package com.zeitungszusteller.app.domain.entity;

import java.sql.Timestamp;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Table(name="delivery_points")
@Builder
public class DeliveryPoint {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	private Long street_id;
	
	@Column(name = "house_number", nullable = false)
	private String houseNumber;
	
	@Enumerated(EnumType.STRING)
	@Column(name = "side")
	private DeliverySide deliverySide;
	
	@Column(name = "last_name", nullable = false)
	private String lastName;

	/** May carry suffixes ('Walter Sen') — nullable in the schema */
	@Column(name = "first_name")
	private String firstName;
	
	/** Free-text delivery note: 'last house on the left', 'BK next to garage', ... */
	private String annotation;

	@Column(nullable = false)
	private Boolean active;
	
	private int version = 0;
	
	@Column(name = "updated_at", nullable = false)
	private Timestamp updatedAt;
	
	// The PostGIS geometry column (geom) is mapped in Phase 5 with hibernate-spatial.
	
	
	
	

}
