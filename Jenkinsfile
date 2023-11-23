node {
    def app
    def dockerImageName

    stage('Clone repository') { // for display purposes
        cleanWs()
        def s = checkout scm
        def splitGitUrl = s.GIT_URL.split('/');
        dockerImageName = splitGitUrl[splitGitUrl.size() - 2] + "/" + splitGitUrl[splitGitUrl.size() - 1].replace(".git", "")
    }
    stage('Build') {
        app = docker.build dockerImageName
    }

    stage('push') {
        withDockerRegistry(credentialsId: 'dockerhub') {
            app.push('latest')
        }

        cleanWs()
    }
}