# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A bank fraud detection project. Currently in early data generation/setup stage with two seed datasets and a stub script for synthetic transaction generation.

## Business Problem checkpoints

1. what are we solving - we are building a fraud detection model to identify the fraud transactions from the dataset. The data is from the banks transaction ledger
2. Fraud cost analysis - The cost of fraud trabsactions are huge per year for this bank
3. Stakeholders - stakeholders art compliance and riskmanagement teams and they want to reduce the losses from the fraus transactions and reduce the time invested to investigate the fraud transaction by reducing the false positives - This is what the success looks like from this model

## DS/ML View of the business problemn

## Data at hand overview

**customers.csv** — customer profiles
- `customer_id` (CUST000001 format), `segment` (young_adult / working_adult / established / retired), `customer_age`, `annual_income`, `credit_score`, `occupation` (Employed / Self-Employed / Retired / Student / Unemployed), `region` (UK regions), `customer_since` (date)

**accounts.csv** — bank accounts linked to customers
- `account_id` (ACC0000001 format), `customer_id`, `account_type` (Current / Savings / etc.), `account_open_date`, `account_balance`, `account_status` (Active / Closed)

## Data Understading

## Data Cleaning

## Feature Engineering

## Model Building

## Hyper parameter tuning

## Model Evaluation

## Business Validation

## Mlops and Deployment

Refactor notebook into modular .py structure
Build training pipeline and inference pipeline
MLflow — experiment tracking and model registry




