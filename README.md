# Kafka-payment-demo
<a name="readme-top"></a>
<!--
*** This README template was copied from https://github.com/othneildrew/Best-README-Template.
-->


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With Python</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#deploying-on-openshift">Deploying on OpenShift</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple project to showcase the use of Kafka as an intermediary for cross service communication, using FastAPI for two services, Balance and Transaction, to simulate a payment transaction. When a transaction is written to the database, the Transaction service also writes a message to a Kafka topic, which is consumed by the Balance service, which then uses the message to update the account balance of the users involved in that transaction.

In this example, the Transaction service is a Kafka Producer, and the Balance service is a Consumer. The Balance service also has Producer capabilities implemented just as a proof of concept to show that it can also write messages. The FastAPI services are mainly used to interact with a database that is using PostGreSQL.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
 
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Ensure Python is installed and of version >3.7
  ```sh
    python --version
    Python 3.12.3
  ```

### Installation #WIP

1. Clone the repo
   ```sh
   git clone https://github.com/Leenoose/Kafka-payment-demo.git
   cd Kafka-payment-demo
   ```
2. Create virtual environment and switch into it for a clean environment to start
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install required dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Ensure you have a PostgreSQL running. If not, use Podman or Docker to run an image.
   ```sh
   podman run -d --name <db-name> -p 5432:5432 -e POSTGRES_PASSWORD=<mypassword> -v /db-init-script.sql:/docker-entrypoint-initdb.d/init.sql postgres:latest
   #The command should run interchangeably with Docker. the -v flag copies the db-init-script.sql into the container and runs it at initialization
   ```
5. Ensure that you have a Kafka Zookeeper and Kafka Server instance running, with a topic created.
   ```sh
   #On your Local machine or a Kafka container
   bin/zookeeper-server-start.sh config/zookeeper.properties

   #On another terminal on your local machine or another Kafka container
   bin/kafka-server-start.sh config/server.properties

   #On another terminal (3) on your local machine or another Kafka container
   bin/kafka-topics.sh --create --topic <event-name> --bootstrap-server localhost:9092
   ```
6. Run the FastAPI server
   ```sh
   uvicorn main:app
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Access the Swagger UI via localhost:8000 (or whichever port you are using for this project) and run the /producer/{topicname} POST request.

After doing so, check your database. The message that was sent in the POST request should have a new entry in the database.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Deploying on OpenShift

To deploy on Red Hat OpenShift, follow the steps as follows.
1. Provisioning Kafka

To provision a Kafka cluster, install the operator AMQ Streams. After doing so, use the Provided APIs to create a Kafka cluster. Feel free to name the cluster however you wish.

2. Provision a PostgreSQL instance

Add two databases via the Developer Catalog, and select PostgreSQL. Note that when doing so, it is important to have a PostgreSQL Connection Username, PostgreSQL Connection Password, and a PostgreSQL Database Name. These will be used in the environment variables. You can call them balance and transaction respectively.

3. Cloning the project

Add the project to your OpenShift console using the git repo url (https://github.com/Leenoose/Kafka-payment-demo.git). As the two services are in subdirectories of their own, expand the advanced Git options, and set the Context dir to /balance and /transaction respectively.

Note that the build for both services will fail. This is because the environment variables are not being set yet, and the default values (localhost) are still being used, even though they are not applicable here. To remedy this, go to Builds, look for the name of the added services, and edit the build config. There should be a section to add environment variables. Update the values as follows

| Name | Value    
| :---:   | :---: 
| KAFKA_HOSTNAME | \<kafka-cluster-url\>   
| DB_HOSTNAME | \<postgres-cluster-url\>
| DB_USER | PostgreSQL Connection username
| DB_PASSWORD | PostgreSQL Connection password
| DB_NAME | PostgreSQL Database Name

For the HOSTNAME variables, refer to the hostname you have under Administrator > Networking > Services.
Click into the individual services and copy the value under Service routing.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Leenoose/FastAPI-Kafka-SQL-Example.svg?style=for-the-badge
[contributors-url]: https://github.com/Leenoose/FastAPI-Kafka-SQL-Example/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Leenoose/FastAPI-Kafka-SQL-Example.svg?style=for-the-badge
[forks-url]: https://github.com/Leenoose/FastAPI-Kafka-SQL-Example/network/members
[stars-shield]: https://img.shields.io/github/stars/Leenoose/FastAPI-Kafka-SQL-Example.svg?style=for-the-badge
[stars-url]: https://github.com/Leenoose/FastAPI-Kafka-SQL-Example/stargazers
[issues-shield]: https://img.shields.io/github/issues/Leenoose/FastAPI-Kafka-SQL-Example.svg?style=for-the-badge
[issues-url]: https://github.com/Leenoose/FastAPI-Kafka-SQL-Example/issues
[license-shield]: https://img.shields.io/github/license/Leenoose/FastAPI-Kafka-SQL-Example.svg?style=for-the-badge
[license-url]: https://github.com/Leenoose/FastAPI-Kafka-SQL-Example/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[PostgreSQL]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
