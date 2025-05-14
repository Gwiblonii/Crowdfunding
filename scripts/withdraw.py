from brownie import Crowdfunding
from scripts.helpful_scripts import get_account

def main():
    crowdfunding = Crowdfunding[-1]
    account = get_account()
    print("Retirando fondos (solo si la meta se cumplió y la campaña terminó)...")

    # Verificaciones opcionales para más seguridad
    time_left = crowdfunding.getTimeLeft()
    total_usd = crowdfunding.getTotalUSD()
    owner = crowdfunding.owner()

    print(f"Tiempo restante: {time_left} segundos")
    print(f"Fondos totales en USD: {total_usd / 1e18:.2f}")
    print(f"Owner del contrato: {owner}")

    if time_left > 0:
        print("⏳ La campaña aún está activa. No se puede retirar.")
        return

    if total_usd < crowdfunding.goal():
        print("❌ La meta no fue alcanzada. No se puede retirar.")
        return

    if account.address != owner:
        print("🚫 Solo el creador del contrato puede retirar los fondos.")
        return

    tx = crowdfunding.withdrawFunds({"from": account})
    tx.wait(1)
    print("✅ Fondos retirados exitosamente.")
