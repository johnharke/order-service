pipeline {
    agent any

    environment {
        // Global variables safely defined as static strings
        REGISTRY    = 'ghcr.io'
        GITHUB_USER = 'johnharke'
        IMAGE_NAME  = 'order-service'
    }

    options {
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/johnharke/order-service.git',
                        credentialsId: 'ghcr-credentials'
                    ]]
                )
                script {
                    // Compute SHORT_SHA dynamically after checkout populates GIT_COMMIT
                    env.SHORT_SHA = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : 'latest'
                }
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "--- Setting up Python virtual environment ---"
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    
                    if [ -f requirements-dev.txt ]; then
                        pip install -r requirements-dev.txt
                    elif [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                    
                    echo "--- Running Pytest ---"
                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def fullImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:${env.SHORT_SHA}"
                    def latestImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:latest"

                    echo "Building container images: ${fullImageTag} and ${latestImageTag}"
                    sh "docker build -t ${fullImageTag} -t ${latestImageTag} ."
                }
            }
        }

        stage('Push to GHCR') {
            steps {
                withCredentials([string(credentialsId: 'ghcr-credentials', variable: 'GHCR_PAT')]) {
                    script {
                        def fullImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:${env.SHORT_SHA}"
                        def latestImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:latest"

                        echo "Logging into GitHub Container Registry..."
                        sh "echo \$GHCR_PAT | docker login ${REGISTRY} -u ${GITHUB_USER} --password-stdin"

                        echo "Pushing image tags to GHCR..."
                        sh "docker push ${fullImageTag}"
                        sh "docker push ${latestImageTag}"
                    }
                }
            }
        }
    }

    post {
        always {
            // Hardcode or handle logout safely without relying on top-level bindings during early crashes
            sh "docker logout ghcr.io || true"
            cleanWs()
        }
        success {
            echo "CI pipeline completed successfully for commit ${env.SHORT_SHA}"
        }
        failure {
            echo "CI pipeline failed."
        }
    }
}