pipeline {
    agent any
    stages {
        stage('Git') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'master']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'CleanBeforeCheckout']],
                    submoduleCfg: [],
                    userRemoteConfigs: [[url: 'your_ssh_url']]
                ])
            }
        }

        stage('deploy') {
            steps {
                sh 'ssh -p your_port your_host "cd your_project_path;git stash;git pull origin master"'
                sh 'ssh -p your_port your_host "cd your_project_path;git stash;git pull origin master"'
            }
        }
    }
}