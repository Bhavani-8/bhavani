@echo off

echo Generating Test Report...
allure generate reports/allure-results --clean -o reports/allure-report
