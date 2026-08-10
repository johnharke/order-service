pipeline {
    agent any

    environment {
        // GitHub Container Registry Settings
        REGISTRY           = 'ghcr.io'
        GITHUB_USER        = 'johnharke'
        IMAGE_NAME         = 'order-service'
        
        // Dynamic Git Short SHA (e.g., db7162d)
        SHORT_SHA          = "${env.GIT_COMMIT.take(7)}"
        
        // Reference to Jenkins Secret Text credential containing your GitHub Personal Access Token (PAT)
        GHCR_CREDS         = credentials('ghcr-credentials')
    }

    options {
        // Skips the implicit checkout on uninitialized default workspace
        skipDefaultCheckout(true)
        // Keeps the 10 most recent builds to conserve disk space
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
                    def fullImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:${SHORT_SHA}"
                    def latestImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:latest"

                    echo "Building container images: ${fullImageTag} and ${latestImageTag}"
                    sh "docker build -t ${fullImageTag} -t ${latestImageTag} ."
                }
            }
        }

        stage('Push to GHCR') {
            steps {
                script {
                    def fullImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:${SHORT_SHA}"
                    def latestImageTag = "${REGISTRY}/${GITHUB_USER}/${IMAGE_NAME}:latest"

                    echo "Logging into GitHub Container Registry..."
                    sh "echo \$GHCR_CREDS | docker login ${REGISTRY} -u ${GITHUB_USER} --password-stdin"

                    echo "Pushing image tags to GHCR..."
                    sh "docker push ${fullImageTag}"
                    sh "docker push ${latestImageTag}"
                }
            }
        }
    }

    post {
        always {
            // Logout of GHCR and clean up workspace artifacts
            sh "docker logout ${REGISTRY} || true"
            cleanWs()
        }
        success {
            echo "CI pipeline completed successfully for commit ${env.SHORT_SHA}"
        }
        failure {
            echo "CI pipeline failed on commit ${env.SHORT_SHA}"
        }
    }
}