# Snowflake Cost Insight Bot

An AI-powered Streamlit tool that helps teams analyze Snowflake query history and warehouse usage to uncover cost-saving opportunities and performance inefficiencies using a Large Language Model (LLM).

---

## 📌 Overview

This project was built for the **KIPI AI/ML Hackathon 2025** with the goal of reducing manual effort in analyzing Snowflake compute usage. The tool connects to Snowflake's `ACCOUNT_USAGE` views, processes query and warehouse metrics, estimates potential cost savings, and uses an LLM to provide actionable insights.

---

## 🔧 Features

- Connects to Snowflake's `ACCOUNT_USAGE` schema
- Analyzes top slow/expensive queries
- Aggregates warehouse utilization over time
- Estimates potential cost savings
- Sends metadata to LLM (Together.ai – Mixtral) for AI-generated recommendations
- Interactive Streamlit dashboard interface
- Supports local `.env` configuration and offline CSV fallback

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/chandraPrakash-tripathi/Hackathon
cd Hackathon
