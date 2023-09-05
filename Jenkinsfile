pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "huseyincece"
        APP_NAME = "helloworld-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${APP_NAME}"
        REGISTRY_CREDS = 'DockerHub'
    }

    stages {
        stage('Cleanup workspace') {
            steps {
                script {
                    cleanWs()
                }
            }
        }

        stage('Checkout SCM') {
            steps {
                script {
                    git credentialsId: 'GitHub',
                        url: 'https://github.com/huseyincece/helloworld.git',
                        branch: 'main'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker_image = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDS) {
                        docker_image.push("${BUILD_NUMBER}")
                        docker_image.push('latest')
                    }
                }
            }
        }

        stage('Delete Docker images') {
            steps {
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker rmi ${IMAGE_NAME}:latest"
            }
        }

        stage('Updating Kubernetes deployment file') {

            steps {
                script {
                    sh """
                    cat deployment.yml
                    sed -i 's/${APP_NAME}.*/${APP_NAME}:${IMAGE_TAG}/g' deployment.yml
                    cat deployment.yml
                    """
                }
            }
        }

        stage('Push the changed deoployment file to Git'){

            steps{
                script{
                    sh """
                    git config --global user.name "huseyincece"
                    git config --global user.email "hsyn.cece@gmail.com"
                    git add deployment.yml
                    git commit -m "updated the deployment file"
                    """
                    withCredentials([gitUsernamePassword(credentialsId: 'GitHub', gitToolName: 'Default')]) {
                        sh "git push https://github.com/huseyincece/helloworld.git main"
                    }
                }
            }
        }
        stage("SSH Into k8s Server") {
            steps{

                script{
                    def remote = [:]
                    remote.name = 'k8s-master-1'
                    remote.host = '192.168.1.35'
                    remote.user = 'k8s-master-1'
                    remote.password = 'k8s-master-1'
                    remote.allowAnyHosts = true

                }
            }
            
        }
       
    }
}
