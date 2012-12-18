employment
==========

Create Jenkins jobs based on if a repo exists in Kiln. This project is intended for people 
who have a large number of projects in kiln and need to automate the process of adding
jobs to test them to Jenkins.

Requirements
------------
Jenkins server installed and running. I have created a [puppet module](https://github.com/CashStar/puppet-jenkins.git) do to do this with.

Jenkins plugins needed
* [greenballs](https://wiki.jenkins-ci.org/display/JENKINS/Green+Balls) *(optional)*
* [ci-game](https://wiki.jenkins-ci.org/display/JENKINS/The+Continuous+Integration+Game+plugin)
* [fogbugz](https://wiki.jenkins-ci.org/display/JENKINS/Fogbugz+Plugin)
* [mercurial](https://wiki.jenkins-ci.org/display/JENKINS/Mercurial+Plugin)
* [cobertura](https://wiki.jenkins-ci.org/display/JENKINS/Cobertura+Plugin)
* [dashboard-view](https://wiki.jenkins-ci.org/display/JENKINS/Dashboard+View) *(optional)*
* [violations](https://wiki.jenkins-ci.org/display/JENKINS/Violations)
* [postbuild-task](http://wiki.hudson-ci.org/display/HUDSON/Post+build+task)
* [envinject](https://wiki.jenkins-ci.org/display/JENKINS/EnvInject+Plugin)
* [thinbackup](https://wiki.jenkins-ci.org/display/JENKINS/thinBackup) *(optional)*
* [build-name-setter](http://wiki.jenkins-ci.org/display/JENKINS/Build+Name+Setter+Plugin)

Installation
------------

Install python dependencies

    pip install -r requirements.txt

Next setup the config file located at employment.conf

    [jenkins]
    url = https://jenkins.<domain>.com
    email = <email address to send jenkins build information to>
    package_prefix = <prefix used to name packaging jenkins jobs>
    upload_script = <full path of script to upload finished package>
    test_script = <full path of script to test projects>
    package_script = <full path of script to package projects>

    [kiln]
    prefix = <ex. <prefix>.kilnhg.com
    username = <kiln username> 
    password = <kiln password

    [group1]
    group_name = <name of the project in kiln>

    projects = <comma seperated list of repos in that project>

    [group2]
    group_name = <name of the project in kiln>

    projects = <comma seperated list of repos in that project>

### Examples

Delete and create development jobs for the 4_0 branch.

    ./run.py -s dev -v 4_0 -d -c

Delete and create development package jobs for the 4_0 branch.

    ./run.py -s dev -v 4_0 -t package -d -c

Delete and create production jobs for the master branch.

    ./run.py -s production -v 4_0 -d -c

Delete and create production jobs for the master branch.

    ./run.py -s production -v 4_0 -d -c

Delete and create production package jobs for the master branch.

    ./run.py -s production -v 4_0 -t package -d -c

TODO
----

Any number of projects, not just two.

Better handling of kiln communication.
