from brownie import Crowdfunding
from scripts.helpful_scripts import get_account
import time

def request_refund():
    crowdfunding = Crowdfunding[-1]
    account = get_account()

    print("Intentando solicitar reembolso...")

    # Confirmamos que la campaña haya terminado y no se haya alcanzado la meta
    time_left = crowdfunding.getTimeLeft()
    total_usd = crowdfunding.getTotalUSD()

    print(f"Tiempo restante: {time_left} segundos")
    print(f"Fondos totales: {total_usd / 1e18:.2f} USD")

    if time_left > 0:
        print("⏳ La campaña aún está activa. Espera a que termine para pedir reembolso.")
        return

    if total_usd >= crowdfunding.goal():
        print("✅ La meta fue alcanzada. No puedes solicitar reembolso.")
        return

    balance_before = account.balance()
    tx = crowdfunding.requestRefund({"from": account})
    tx.wait(1)
    balance_after = account.balance()

    print(f"Reembolso exitoso. Balance antes: {balance_before}, después: {balance_after}")

def main():
    request_refund()
