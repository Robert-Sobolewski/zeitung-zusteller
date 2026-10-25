package com.zeitungszusteller.app.domain.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * Newspaper type as printed in the Tagesliste, e.g. 'ME-OBB'.
 * The schema has NO surrogate id — code is the natural primary key.
 */
@Entity
@Table(name = "newspaper_types")
public class NewspaperType {

	@Id
	private String code;

	private String name;
}
