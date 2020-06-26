Design of a scrapper and proxies tester as a Proof of Proficiency test requested by a company.

----------- WITHOUT-DOCKER -----------

USAGE : python3 scraproxy.py [FLAG (optional)] [NBR (optional)]

FLAGS :
  [-clean]        : delete list.csv and working.csv
  [-startandshow] : run scraproxy and display list.csv and working.csv at the end (could work with or without [NBR])
  [-startonly]    : run scraproxy with or without [NBR]

----------- WITH-DOCKER -----------

RUN   :  sudo docker build -t scraproxy [PATH to DOCKERFILE]

USAGE : sudo docker run scraproxy [FLAG]

FLAGS :
  [-clean]        : delete list.csv and working.csv
  [-startandshow] : run scraproxy and display list.csv and working.csv at the end (could work with or without [NBR])
  [-startonly]    : run scraproxy with or without [NBR]

-----------------------------------

Objective 1: You are asked to write a scrapper that will retrieve
            a list of proxy socks4/socks5/HTTP/HTTPS. There are sites
            that list open proxies:
              https://hidemy.name/en/proxy-list
              https://proxyscrape.com/free-proxy-list
              http://free-proxy.cz/en/proxylist

            The list of proxies must be written in a "list.csv" file.
            in the format: PROXY_TYPE;IP;PORT
            for example: "socks4;1.1.1.1.1;4578".


Objective 2: Once this proxy list has been built, you are asked to
            test them and build a second list in a
            "working.csv" having the same format as the "list.csv" file.

            The "working.csv" file will therefore only contain functional proxies.
            For example in bash "curl --socks4 IP:PORT https://ipinfo.io" must
            return the IP of the proxy being tested.

            Prerequisite:

            * Use the language of your choice (Java/Python/Go/C/C++/C#/Rust)

            * Use docker or podman

            * Bonus: Think of the principle of least privilege that applies to containers.

            Deliverable:

            * A Dockerfile with the script(s)/source(s)/program(s) that fills the
              objectives (in a zip or tar.gz)

            * Report explaining your path, the blocking points and the points
              strong of your realization (in PDF)

            Checking:

            To verify we will make the following orders:

                docker build... && docker run ...
                OR
                podman build ... && podman run ...

            And we'll go run a "cat working.csv" at the place where you
            will have saved the file in the container.

            Translated with www.DeepL.com/Translator (free version)

Deadline: 10 days
