from ortools.sat.python import cp_model
import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Synthetic Data Generator
# ----------------------------
def generate_synthetic_data():
    np.random.seed(42)
    demand = np.random.randint(100, 1000, size=8)
    bus_capacity = 50
    max_buses = 20
    traffic_delay = np.random.randint(0, 30, size=8)
    return demand, bus_capacity, max_buses, traffic_delay

# ----------------------------
# Baseline Model
# ----------------------------
def baseline_model(demand, bus_capacity, max_buses):
    model = cp_model.CpModel()
    buses = [model.NewIntVar(0, max_buses, f'b_{t}') for t in range(8)]
    waiting_time = [model.NewIntVar(0, 1000, f'w_{t}') for t in range(8)]

    for t in range(8):
        model.Add(waiting_time[t] >= demand[t] - buses[t] * bus_capacity)
        model.Add(waiting_time[t] >= 0)
        model.Add(buses[t] <= max_buses)

    model.Minimize(sum(waiting_time[t] * 15 + buses[t] * 100 for t in range(8)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        return {
            "buses": [solver.Value(buses[t]) for t in range(8)],
            "waiting_time": [solver.Value(waiting_time[t]) for t in range(8)],
        }
    else:
        raise ValueError("No optimal solution found for the baseline model.")

# ----------------------------
# Extended Model (Fixed)
# ----------------------------
def extended_model(demand, bus_capacity, max_buses, traffic_delay):
    model = cp_model.CpModel()
    buses = [model.NewIntVar(0, max_buses, f'b_{t}') for t in range(8)]
    waiting_time = [model.NewIntVar(0, 30, f'w_{t}') for t in range(8)]
    emissions = [model.NewIntVar(0, 1000, f'e_{t}') for t in range(8)]
    emission_factor = 10

    for t in range(8):
        model.Add(waiting_time[t] >= demand[t] - buses[t] * bus_capacity)
        model.Add(emissions[t] == buses[t] * emission_factor)
        model.Add(buses[t] <= max_buses)
        if t < 7:
            delay_penalty = traffic_delay[t] // 10
            temp = model.NewIntVar(0, max_buses, f'delay_effect_{t}')
            model.Add(temp == buses[t] - delay_penalty)
            model.Add(buses[t + 1] >= temp)

    model.Minimize(sum(waiting_time[t] * 15 + buses[t] * 100 + emissions[t] * 5 for t in range(8)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        return {
            "buses": [solver.Value(buses[t]) for t in range(8)],
            "waiting_time": [solver.Value(waiting_time[t]) for t in range(8)],
            "emissions": [solver.Value(emissions[t]) for t in range(8)],
        }
    else:
        raise ValueError("No optimal solution found for the extended model.")

# ----------------------------
# Streamlit App
# ----------------------------
def main():
    st.set_page_config(layout="wide")
    st.title("🚌 Optimizing Public Bus Network Scheduling")
    st.sidebar.header("⚙️ Settings")

    demand, bus_capacity, max_buses, traffic_delay = generate_synthetic_data()

    st.sidebar.write("**Passenger Demand:**", demand)
    st.sidebar.write("**Bus Capacity:**", bus_capacity)
    st.sidebar.write("**Max Buses Available:**", max_buses)
    st.sidebar.write("**Traffic Delays (mins):**", traffic_delay)

    if st.sidebar.button("🚀 Run Baseline Model"):
        results = baseline_model(demand, bus_capacity, max_buses)
        st.success("✅ Baseline Model Results")
        df = pd.DataFrame({
            "Hour": list(range(8)),
            "Buses Deployed": results["buses"],
            "Waiting Time (mins)": results["waiting_time"]
        })
        st.markdown("### 📊 Buses Deployed and Waiting Time:")
        st.dataframe(df)

    if st.sidebar.button("🔧 Run Extended Model"):
        results = extended_model(demand, bus_capacity, max_buses, traffic_delay)
        st.success("✅ Extended Model Results")
        df = pd.DataFrame({
            "Hour": list(range(8)),
            "Buses Deployed": results["buses"],
            "Waiting Time (mins)": results["waiting_time"],
            "Emissions (kg CO2)": results["emissions"]
        })
        st.markdown("### 📊 Buses Deployed, Waiting Time, and Emissions:")
        st.dataframe(df)

        hours = list(range(8))
        buses = results["buses"]
        wait = results["waiting_time"]
        emissions = results["emissions"]

        # 📊 Line Plot
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(hours, buses, marker='o', label="Buses Deployed")
        ax1.plot(hours, wait, marker='x', label="Waiting Time (mins)", color='orange')
        ax1.plot(hours, emissions, marker='s', label="Emissions (kg CO₂)", color='green')
        ax1.set_title("Extended Model: Buses, Waiting Time, and Emissions")
        ax1.set_xlabel("Hour")
        ax1.set_ylabel("Count / Minutes / CO₂")
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

        # 📊 Wait Time Bar
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.bar(hours, wait, color='orange')
        ax2.set_title("Passenger Waiting Time per Hour")
        ax2.set_xlabel("Hour")
        ax2.set_ylabel("Waiting Time (mins)")
        st.pyplot(fig2)

        # 📊 Emissions Bar
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.bar(hours, emissions, color='green')
        ax3.set_title("CO₂ Emissions per Hour")
        ax3.set_xlabel("Hour")
        ax3.set_ylabel("Emissions (kg)")
        st.pyplot(fig3)

        # 📊 Efficiency Line
        efficiency = [b / w if w > 0 else 0 for b, w in zip(buses, wait)]
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        ax4.plot(hours, efficiency, marker='d', linestyle='--', label="Buses per Minute Wait Time")
        ax4.set_title("Operational Efficiency")
        ax4.set_xlabel("Hour")
        ax4.set_ylabel("Buses / Wait Minute")
        ax4.legend()
        ax4.grid(True)
        st.pyplot(fig4)

        # 📊 Stacked Area
        fig5, ax5 = plt.subplots(figsize=(8, 4))
        ax5.stackplot(hours, buses, emissions, labels=["Buses", "Emissions"], colors=["#1f77b4", "#2ca02c"])
        ax5.set_title("Stacked Area: Buses & Emissions")
        ax5.set_xlabel("Hour")
        ax5.set_ylabel("Value")
        ax5.legend(loc="upper left")
        st.pyplot(fig5)

    # 📍 Route Map
    st.markdown("### 🗺️ Route Visualization")
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)
    folium.Marker([12.9716, 77.5946], popup="Central Station", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([12.9352, 77.6245], popup="Route 1 Stop").add_to(m)
    folium.Marker([12.9784, 77.6408], popup="Route 2 Stop").add_to(m)
    folium_static(m)

if __name__ == "__main__":
    main()



