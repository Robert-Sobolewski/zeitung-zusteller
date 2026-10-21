// Zeitungszusteller Platform — pipeline CI/CD (Jenkins)
pipeline {
    agent any

    environment {
        COMPOSE_PROJECT = 'zeitung-zusteller'
    }

    stages {
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

        // Faza 1+: etapy testów (mvn test, vitest, pytest) — po dodaniu testów
    }

    post {
        failure {
            echo 'Pipeline failed — zobacz logi powyżej.'
        }
    }
}
