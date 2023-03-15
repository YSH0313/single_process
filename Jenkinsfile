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
                    userRemoteConfigs: [[url: 'git@gitlab.bailian-ai.com:yuanshaohang/single_process.git']]
                ])
            }
        }

        stage('deploy') {
            steps {
                sh 'ssh -p 11000 bailian@172.17.48.132 "cd /home/bailian/single_process;git stash;git pull origin master"'
                sh 'ssh -p 11000 bailian@172.17.167.26 "cd /home/bailian/single_process;git stash;git pull origin master"'
            }
        }
    }
}