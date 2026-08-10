pipeline {
    agent any

    environment {
        IMAGE_REPOSITORY = "ghcr.io/johnharke/order-service"
        IMAGE_TAG = "${GIT_COMMIT}"
        IMAGE = "${IMAGE_REPOSITORY}:${IMAGE_TAG}"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements-dev.txt
                    pytest
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE} \
                      .
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-credentials',
                        usernameVariable: 'GHCR_USER',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "${GHCR_TOKEN}" | docker login ghcr.io \
                          -u "${GHCR_USER}" \
                          --password-stdin

                        docker push ${IMAGE}

                        docker logout ghcr.io
                    '''
                }
            }
        }
    }
}
