import numpy as np
import streamlit as st

def simulate_machine(commands, T, theta, beta, eta):
    total_time = 0
    next_maintenance = T

    for tau_j in commands:
        while tau_j > 0:  
            time_to_failure = np.random.weibull(beta) * eta
            if total_time + time_to_failure >= next_maintenance:
                total_time = next_maintenance + theta
                next_maintenance += T
            else:
                if time_to_failure >= tau_j:
                    total_time += tau_j
                    tau_j = 0
                else:
                    total_time += time_to_failure
                    tau_j -= time_to_failure
                    repair_time = theta / 2  
                    total_time += repair_time

    return total_time

def replicate_simulations(r, commands, T, theta, beta, eta):
    delays = [simulate_machine(commands, T, theta, beta, eta) for _ in range(r)]
    return delays

st.markdown("""
    <style>
        .signature {
            font-size: 24px;
            font-weight: bold;
            color: #2e3a87;
            text-align: center;
            font-family: 'Arial', sans-serif;
            padding: 20px;
            border-top: 3px solid #2e3a87;
            margin-top: 20px;
        }
    </style>
    <div class="signature">par MOHAMED ABID</div>
""", unsafe_allow_html=True)
st.title("Simulation de délai total (Ω) pour les commandes sur une machine sujette à pannes")
st.sidebar.header("Paramètres de simulation")
T = st.sidebar.number_input("Période de maintenance préventive (T)", value=1000, min_value=100, step=100)
theta = st.sidebar.number_input("Durée de maintenance préventive (θ)", value=2.0, min_value=0.1, step=0.1)
beta = st.sidebar.number_input("Paramètre de forme Weibull (β)", value=1.8, min_value=0.1, step=0.1)
eta = st.sidebar.number_input("Paramètre d'échelle Weibull (η)", value=900, min_value=100, step=50)
r = st.sidebar.slider("Nombre de réplications (r)", min_value=100, max_value=5000, value=1000, step=100)

st.sidebar.subheader("Durées des commandes (τ_j)")
commands_input = st.sidebar.text_area("Entrez les durées des commandes séparées par des virgules :", "240,120,80,200,320,260,150,180,400,300")
commands = list(map(int, commands_input.split(',')))

if st.sidebar.button("Lancer la simulation"):
    with st.spinner("Simulation en cours..."):
        delays = replicate_simulations(r, commands, T, theta, beta, eta)
        mean_delay = np.mean(delays) 
        std_delay = np.std(delays)  
    st.success("Simulation terminée !")
    st.write(f"### Résultats de la simulation ({r} réplications)")
    st.write(f"- **Valeur moyenne de Ω :** {mean_delay:.2f} heures")
    st.write(f"- **Écart-type de Ω :** {std_delay:.2f} heures")

    st.write("### Distribution des délais simulés (Ω)")
    st.bar_chart(np.histogram(delays, bins=20)[0])


