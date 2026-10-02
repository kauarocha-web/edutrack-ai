credito = float(input('Seu credito : R$'))
while  credito > 0 :
    item = float(input('Preco do item: R$ '))
    if item > credito:

        print('Compra negada! Ultrapassa seu credito ')
        break
    credito -= item 
print(f'voce zerou sua carteira')