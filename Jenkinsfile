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

                    }
                    else {

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

            // Publish HTML Report
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'API Automation Report'
            ])

            // Publish Allure Report
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }

        success {

            // Send SUCCESS email
            emailext(
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

Jenkins API Automation build completed successfully.

================================
BUILD INFORMATION
================================

Job Name    : ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Status      : SUCCESS

Environment : ${params.ENV}
Test Suite  : ${params.TEST_SUITE}

================================
REPORTS
================================

Jenkins Build:
${env.BUILD_URL}

HTML Report:
${env.BUILD_URL}API_20Automation_20Report/

Allure Report:
${env.BUILD_URL}allure/

Regards,
Jenkins
""",
                to: 'pranjalnanda406@gmail.com'
            )
        }

        failure {

            // Send FAILURE email
            emailext(
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

Jenkins API Automation build has FAILED.

================================
BUILD INFORMATION
================================

Job Name    : ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Status      : FAILURE

Environment : ${params.ENV}
Test Suite  : ${params.TEST_SUITE}

================================
CHECK BUILD
================================

Jenkins Build:
${env.BUILD_URL}

Please check the Jenkins Console Output for the failure details.

Regards,
Jenkins
""",
                to: 'pranjalnanda406@gmail.com'
            )
        }
    }
}