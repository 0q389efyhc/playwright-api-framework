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

                    withCredentials([
                        string(
                            credentialsId: 'qase-api-token',
                            variable: 'QASE_TESTOPS_API_TOKEN'
                        )
                    ]) {

                        if (params.TEST_SUITE == 'all') {

                            bat '''
                            set QASE_MODE=testops
                            set QASE_TESTOPS_PROJECT=ECOM
                            set QASE_ENVIRONMENT=%ENV%

                            venv\\Scripts\\python -m pytest -v --html=reports/report.html --self-contained-html --alluredir=allure-results
                            '''

                        }
                        else {

                            bat """
                            set QASE_MODE=testops
                            set QASE_TESTOPS_PROJECT=ECOM
                            set QASE_ENVIRONMENT=%ENV%

                            venv\\Scripts\\python -m pytest -v -m ${params.TEST_SUITE} --html=reports/report.html --self-contained-html --alluredir=allure-results
                            """
                        }
                    }
                }
            }
        }
    }

    post {

        always {

            // Publish HTML Report
            publishHTML([
                allowMissing: true,
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

            mail(
                to: 'pranjalnanda406@gmail.com',
                from: 'pranjalnanda406@gmail.com',
                replyTo: 'pranjalnanda406@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

Jenkins API Automation build completed successfully.

Job Name     : ${env.JOB_NAME}
Build Number : #${env.BUILD_NUMBER}
Status       : SUCCESS

Environment  : ${params.ENV}
Test Suite   : ${params.TEST_SUITE}

Jenkins Build:
${env.BUILD_URL}

HTML Report:
${env.BUILD_URL}API_20Automation_20Report/

Allure Report:
${env.BUILD_URL}allure/

Qase Project:
ECOM

Regards,
Jenkins
"""
            )
        }

        failure {

            mail(
                to: 'pranjalnanda406@gmail.com',
                from: 'pranjalnanda406@gmail.com',
                replyTo: 'pranjalnanda406@gmail.com',
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

Jenkins API Automation build has FAILED.

Job Name     : ${env.JOB_NAME}
Build Number : #${env.BUILD_NUMBER}
Status       : FAILURE

Environment  : ${params.ENV}
Test Suite   : ${params.TEST_SUITE}

Jenkins Build:
${env.BUILD_URL}

Please check the Jenkins Console Output and Qase for details.

Regards,
Jenkins
"""
            )
        }

        cleanup {

            echo 'Cleaning Jenkins workspace...'

            deleteDir()
        }
    }
}