# Altitude-based Deployment Logic

## Goal

Avoid triggering parachute deployment from a single noisy altitude measurement.

## Verified Decision Structure

1. reject clearly invalid altitude values
2. compute a moving average over recent altitude samples
3. require altitude to be above a minimum deployment threshold
4. compare consecutive moving-average values
5. reset the falling counter if the trend reverses
6. deploy only after multiple consecutive downward checks

## Parameters Observed in the Team Implementation

| Parameter | Value |
|---|---:|
| moving-average window | 10 samples |
| minimum deployment altitude | 100 m |
| consecutive falling checks | 5 |

## Important Limitation

The original codebase also contained attitude-related and location-related functions.
Those paths were not active final deployment triggers in the verified code and are therefore not presented as completed features here.
