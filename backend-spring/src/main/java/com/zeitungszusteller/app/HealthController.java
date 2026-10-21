package com.zeitungszusteller.app;

import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Health endpoint — używany przez docker-compose healthcheck i frontend.
 */
@RestController
public class HealthController {

    private final JdbcTemplate jdbc;

    public HealthController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/health")
    public Map<String, Object> health() {
        boolean dbUp = true;
        try {
            jdbc.queryForObject("SELECT 1", Integer.class);
        } catch (Exception e) {
            dbUp = false;
        }
        return Map.of(
                "status", dbUp ? "UP" : "DEGRADED",
                "service", "backend-spring",
                "database", dbUp ? "connected" : "disconnected"
        );
    }
}
