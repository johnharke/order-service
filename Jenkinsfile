pipeline {
    agent {
        node {
            label ''
            customWorkspace '/var/jenkins_home/workspace/order-service'
        }
    }
    
    options {
        skipDefaultCheckout(true)
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
                sh 'echo "Workspace cleanly initialized!"'
            }
        }
    }
}