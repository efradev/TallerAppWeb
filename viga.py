import math
import pandas as pd

def calculoFlexion(
    b,
    h,
    fc,
    fy,
    Es,
    Ecu,
    phiFlexion,
    acero,
    r
):
    
    ####### Cálculos generales #############

    # Cálculo del factor beta1
    if fc <= 280:
        beta1 = 0.85
    elif fc <= 560:
        beta1 = round(1.05 - 0.714 * (fc / 1000), 3)
    else:
        beta1 = 0.65

    # Cálculo de la deformación inicial del concreto comprimido
    E0 = round(Ecu * (1 - beta1), 5)

    ### 1.1 Cálculo de acero minimo############

    d = h - r

    aceroMinimo = 0.7 * ((math.sqrt(fc)) / (fy)) * b * d

    ###1.2 Acero balanceado y acero máximo
    aceroBalanceado = (
        b * d * (0.85 * beta1 * fc / fy) * ((Ecu) / (Ecu + fy / Es))
    )
    aceroMaximo = 0.75 * aceroBalanceado

    if  acero < aceroBalanceado:
        ###1.3 Calculo de a, c y Mn

        ### Asumiendo que el acero fluye (se debe verificar)
        T = acero * fy
        a = T / (0.85 * fc * b)
        c = a / beta1
        Mn = T * (d - a / 2) / (1000 * 100)
        phiMn = phiFlexion * Mn

    else:
        A = (0.85 * fc) / (Ecu * Es * (acero / (b * d)))
        B = d
        C = -beta1 * d * d

        a = (
            -B
            + math.sqrt(B * B - 4 * A * C)
        ) / (2 * A)

        c = a / beta1

        Mn = (0.85 * fc * a * b * (d - a / 2) / (1000 * 100)
        )
        phiMn = phiFlexion * Mn   

    if round(acero,2) < round(aceroBalanceado,2):
        tipoFalla = "Tracción"
    elif round(acero,2) > round(aceroBalanceado,2):
        tipoFalla = "Compresión"
    else:
        tipoFalla = "Balanceada"
        
    defAs = Ecu * (d-c)/c
    
    
    resultado = {}
    resultado["aceroMinimo"] = f'{round(aceroMinimo, 2)} cm^2'
    resultado["aceroBalanceado"] = f'{round(aceroBalanceado, 2)} cm^2'
    resultado["aceroMaximo"] = f'{round(aceroMaximo, 2)} cm^2'
    resultado["a"] = f'{round(a, 2)} cm'
    resultado["c"] = f'{round(c, 2)} cm'
    resultado["Mn"] = f'{round(Mn, 2)} ton-m'
    resultado["phiMn"] = f'{round(phiMn, 2)} ton-m'
    resultado["tipoFalla"] = tipoFalla
    resultado["defAs"] = f'{round(defAs, 5)}'
    resultado["c_value"] = c

    return resultado


tablaAceros = pd.DataFrame(
    {
        "Diametro": [
            "6mm",
            '1/4"',
            "8mm",
            '3/8"',
            "12mm",
            '1/2"',
            '5/8"',
            '3/4"',
            '1"',
            '1 3/8"',
        ],
        "Área(cm2)": [0.28, 0.32, 0.5, 0.71, 1.13, 1.29, 2, 2.84, 5.1, 10.06],
    }
)
#tablaAceros = tablaAceros.set_index("Diametro")

def areaAs (numero, diametro):
    return numero * tablaAceros.loc[tablaAceros['Diametro'] == diametro, "Área(cm2)"].values[0] 