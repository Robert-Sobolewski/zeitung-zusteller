// Zeitungszusteller Platform — pipeline CI/CD (Jenkins)
pipeline {
    agent any

    environment {
        COMPOSE_PROJECT = 'zeitung-zusteller'
    }

    stages {
        // Cheapest tests first: fail fast before spending minutes on image builds.
        stage('Unit tests') {
            steps {
                // ai-pipeline: parser tests inside the service image; real-data mounted (never baked in)
                sh 'docker compose run --rm -v "${WORKSPACE}/real-data:/real-data" ai-pipeline python -m pytest'
                // backend-spring: mvn test in a Maven container; Docker socket for Testcontainers,
                // named volume caches ~/.m2 between runs, RYUK disabled (no sidecar pull needed)
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}:/work" -w /work/backend-spring \
                        -v maven-cache:/root/.m2 \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -e DOCKER_HOST=unix:///var/run/docker.sock \
                        -e RYUK_DISABLED=true \
                        maven:3.9-eclipse-temurin-21 mvn test
                '''
            }
        }

        stage('Build images') {
            steps {
                sh 'docker compose build --quiet'
            }
        }

        stage('Healthcheck') {
            steps {
                sh '''
                    docker compose up -d --timeout 180
                    until curl -sf http://localhost:8080/api/health; do sleep 3; done
                    curl -sf http://localhost:8000/health
                    echo "All services healthy"
                '''
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed — zobacz logi powyżej.'
        }
    }
}
