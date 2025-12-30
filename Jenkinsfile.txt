pipeline {
    agent any

    /* -----------------------------
       PARAMETERS (Step 12)
       ----------------------------- */
    parameters {
        booleanParam(name: 'executeTests', defaultValue: true, description: 'Run test stage?')
    }

    /* -----------------------------
       ENVIRONMENT VARIABLES (Step 10)
       ----------------------------- */
    environment {
        VERSION = '1.0.0'
    }

    /* -----------------------------
       BUILD TOOLS (Step 11)
       ----------------------------- */
    tools {
        maven 'Maven'
    }

    stages {

        /* -----------------------------
           BUILD STAGE
           ----------------------------- */
        stage('Build') {
            steps {
                echo "Building.."
                bat 'mvn -version'    // Just to show Maven works
            }
        }

        /* -----------------------------
           TEST STAGE WITH CONDITION
           (Step 9 - Conditional Execution)
           ----------------------------- */
        stage('Test') {
            when {
                expression { params.executeTests == true }
            }
            steps {
                echo "Testing.."
            }
        }

        /* -----------------------------
           DEPLOY STAGE
           ----------------------------- */
        stage('Deploy') {
            steps {
                echo "Deploying.."
                echo "App Version: ${VERSION}"
            }
        }
    }

    /* -----------------------------
       POST-BUILD ACTIONS (Step 8)
       ----------------------------- */
    post {
        always {
            echo 'Pipeline Completed'
        }
    }
}
