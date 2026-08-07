pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/0q389efyhc/playwright-api-framework.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                C:\\Users\\Admin\\playwright-api-framework\\venv\\Scripts\\pip.exe install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                C:\\Users\\Admin\\playwright-api-framework\\venv\\Scripts\\python.exe -m pytest -v --html=reports/report.html --self-contained-html
                '''
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
        }
    }
}