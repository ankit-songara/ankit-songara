<div align="center">

<a href="https://ankit-songara.github.io">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=26&pause=1200&color=58A6FF&center=true&vCenter=true&width=720&height=45&lines=Backend+Engineer+%40+Razorpay;Go+%7C+Distributed+Systems+%7C+Payments;I+build+services+that+move+money+safely.;Trying+hands+on+open-source." alt="Backend Engineer @ Razorpay" />
</a>

<br />

[![Portfolio](https://img.shields.io/badge/Portfolio-0D1117?style=for-the-badge&logo=googlechrome&logoColor=58A6FF&labelColor=0D1117)](https://ankit-songara.github.io)
[![Followers](https://img.shields.io/github/followers/ankit-songara?style=for-the-badge&logo=github&logoColor=white&color=0D1117&labelColor=0D1117)](https://github.com/ankit-songara?tab=followers)
[![Stars](https://img.shields.io/github/stars/ankit-songara?style=for-the-badge&logo=github&logoColor=white&color=0D1117&labelColor=0D1117&affiliations=OWNER)](https://github.com/ankit-songara?tab=repositories)
![Visitors](https://komarev.com/ghpvc/?username=ankit-songara&style=for-the-badge&color=58A6FF&label=VISITORS)

</div>

---

```console
ankit@razorpay:~$ whoami

  name       : Ankit Songara
  role       : Backend Engineer @ Razorpay
  location   : India
  domain     : payments · fintech · distributed systems
  daily      : Go, PostgreSQL, Kafka, Redis, Docker
  building   : disbursement rails, LLD systems, dev tooling
  learning   : Go internals, queueing theory, system design
  ask me     : microservices, payment state machines, LLD

ankit@razorpay:~$ _
```

---

## `~/` Tech Stack

<div align="center">

**Languages**

![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)

**Backend & Data**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=flat-square&logo=nestjs&logoColor=white)
![Gin](https://img.shields.io/badge/Gin-008ECF?style=flat-square&logo=gin&logoColor=white)

**Infra & Observability**

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

</div>

---

## `~/` Selected Work

#### [`disbursement-service`](https://github.com/ankit-songara/disbursement-service) &nbsp; ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/ankit-songara/disbursement-service?style=flat-square&color=161B22&labelColor=0D1117)

Loan disbursement microservice built the way payment rails actually work: the HTTP API answers in under 100 ms and hands off to a worker queue, channels are tried in order (UPI → IMPS → NEFT), and settlement arrives by bank callback rather than polling. State machine per disbursement, circuit breakers per channel, exponential-backoff retries, reconciliation against bank statements, Prometheus metrics and Grafana dashboards.

#### [`coldreach`](https://github.com/ankit-songara/coldreach) &nbsp; ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/ankit-songara/coldreach?style=flat-square&color=161B22&labelColor=0D1117)

Cold-email pipeline that treats a job search as a funnel instead of a lottery — hunt contacts, verify deliverability, draft against your résumé, send from your own Gmail with pacing and caps, then track every lead from *sent → reply → interview → offer* and surface which sources actually convert. Self-hosted: your Gmail, your LLM, your data. → [live demo](https://coldreach-psi.vercel.app)

#### [`lift-elevator-lld`](https://github.com/ankit-songara/lift-elevator-lld) &nbsp; ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/ankit-songara/lift-elevator-lld?style=flat-square&color=161B22&labelColor=0D1117)

Elevator control system where each lift runs on its own goroutine, state is mutex-guarded, and routing uses the SCAN algorithm so no floor starves. A low-level design exercise taken far enough to actually run concurrently.

#### [`parking-lot-system`](https://github.com/ankit-songara/parking-lot-system) &nbsp; ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/ankit-songara/parking-lot-system?style=flat-square&color=161B22&labelColor=0D1117)

Multi-floor, multi-vehicle parking lot: nearest-spot assignment, spot-size compatibility rules, pluggable pricing via the Strategy pattern, and thread-safe ticketing under concurrent entry and exit.

#### [`installement-service`](https://github.com/ankit-songara/installement-service) &nbsp; ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/ankit-songara/installement-service?style=flat-square&color=161B22&labelColor=0D1117)

Buy-now-pay-later checkout — per-customer credit limits enforced in real time, purchases split into tracked installment plans, and idempotency keys so a retried request never double-charges.

#### [`monthly-tracker`](https://github.com/ankit-songara/monthly-tracker) &nbsp; ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/ankit-songara/monthly-tracker?style=flat-square&color=161B22&labelColor=0D1117)

Expense tracking with no app and no cloud: text a Telegram bot *"spent 500 on ola"*, it parses the sentence, categorises it, writes to local SQLite and regenerates an offline HTML dashboard. Nothing ever leaves your machine.

---

## `~/` Currently Working On

<!-- ACTIVITY:START -->
| | repo | when |
| --- | --- | --- |
| `started` | [**ankit-songara**](https://github.com/ankit-songara/ankit-songara) | 6m ago |
| `pushed to` | [**coldreach**](https://github.com/ankit-songara/coldreach) | 37m ago |

<sub>Auto-generated from the GitHub API · last refreshed 28 Aug 2026, 05:46 UTC</sub>
<!-- ACTIVITY:END -->

---

## `~/` Language Breakdown

<!-- LANGS:START -->
```text
primary language across 15 original repos

Go          ██████████░░░░░░░░░░░░░░░░   6 repos
Python      ███████░░░░░░░░░░░░░░░░░░░   4 repos
HTML        █████░░░░░░░░░░░░░░░░░░░░░   3 repos
C++         ██░░░░░░░░░░░░░░░░░░░░░░░░   1 repo
TypeScript  ██░░░░░░░░░░░░░░░░░░░░░░░░   1 repo
```

<sub>Auto-generated from the GitHub API · last refreshed 28 Aug 2026, 05:46 UTC</sub>
<!-- LANGS:END -->

---

## `~/` Streak

<div align="center">

<img width="60%" src="https://streak-stats.demolab.com?user=ankit-songara&theme=tokyonight&hide_border=true&background=0D1117&ring=58A6FF&fire=58A6FF&currStreakLabel=58A6FF" alt="GitHub streak" />

</div>

---

## `~/` Contribution Snake

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ankit-songara/ankit-songara/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ankit-songara/ankit-songara/output/github-snake.svg" />
  <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/ankit-songara/ankit-songara/output/github-snake.svg" />
</picture>

</div>

---

<div align="center">

```console
ankit@razorpay:~$ echo "open to talking about Go, payments infra and system design"
```

<sub>This README builds itself — snake redrawn every 12h, activity and language stats regenerated every 6h straight from the GitHub API.</sub>

</div>
