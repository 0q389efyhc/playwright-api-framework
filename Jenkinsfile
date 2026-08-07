pipeline {

    agent any

    parameters {

        choice(
            name: 'ENV',
            choices: ['QA', 'UAT', 'PROD'],
            description: 'Select Environment'
        )

        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression'],
            description: 'Select Test Suite'
        )
    }

    stages {

        stage('Create Venv') {
            steps {
                bat 'C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Set Environment') {
            steps {
                script {

                    if (params.ENV == 'QA') {
                        env.BASE_URL = 'https://jsonplaceholder.typicode.com'
                    }
                    else if (params.ENV == 'UAT') {
                        env.BASE_URL = 'https://jsonplaceholder.typicode.com'
                    }
                    else {
                        env.BASE_URL = 'https://jsonplaceholder.typicode.com'
                    }

                    echo "Running on ${env.BASE_URL}"
                }
            }
        }

        stage('Run Tests') {
            steps {

                script {

                    if (params.TEST_SUITE == 'all') {

                        bat '''
                        venv\\Scripts\\python -m pytest -v --html=reports/report.html --self-contained-html --alluredir=allure-results
                        '''

                    } else {

                        bat """
                        venv\\Scripts\\python -m pytest -v -m ${params.TEST_SUITE} --html=reports/report.html --self-contained-html --alluredir=allure-results
                        """

                    }

                }

            }
        }

    }

    post {

        always {

            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'API Automation Report'
            ])

            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])

        }

    }

}