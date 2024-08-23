#!/bin/groovy
pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
        buildDiscarder(logRotator(numToKeepStr: "5"))
    }
    stages {
        stage('Install Environment') {
            when {
                expression {
                fileExists('env/bin/activate') == false
                }
            }
            steps {
                script {
                    sh """
                    echo 'creating virtualenv...'
                    virtualenv env
                    . ./env/bin/activate
                    export TESTS=True;pip install -e .
                    """
                }
            }
        }
        stage('Lint') {
            steps {
                sh """
                echo 'Running Linting'
                chmod +x ./tools/lint.sh
                """
                sshagent (['calbright_github_2']) {
                    echo 'fetching remote main for flake comparison'
                    sh """
                    git config --unset-all remote.origin.fetch
                    git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
                    git fetch --all
                    git stash
                    git checkout main
                    git checkout "${env.BRANCH_NAME}"
                    git config pull.rebase false
                    git pull
                    . ./env/bin/activate
                    ./tools/lint.sh -x flake8 -b main
                    """
                    }
            }
        }
        stage('Unit Tests') {
            failFast true
            steps {
                sshagent (['calbright_github_2']) {
                    sh """
                    . ./env/bin/activate
                    export PYTHONPATH=${pwd()}; python tools/start_tests.py
                    """
                }
            }
            post {
                always {
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main';
                }
            }
            steps {
                script {
                    withCredentials([aws(accessKeyVariable:'AWS_ACCESS_KEY_ID', credentialsId: 'AWS Credentials', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        sh """
                        . ./env/bin/activate

                        # Checking if there are DB migrations to be applied to stage
                        CHANGED=`git diff --name-only \$GIT_PREVIOUS_COMMIT \$GIT_COMMIT propus/calbright_sql/alembic/versions`
                        if [ ! -z "\$CHANGED" ]; then
                            echo "Changes detected. Deploying alembic changes"
                            ENV=stage bash tools/run_calbright_alembic.sh
                            ENV=prod bash tools/run_calbright_alembic.sh
                        fi
                        """
                    }
                }
            }
        }
    }
    post {
      always {
        cleanWs()
      }
    }
}