import matplotlib.pyplot as plt

accuracy = [0.4414634147310645, 0.4548780487804878, 0.4634146343401777, 0.4691056910084515, 0.48048780516880313, 0.48983739847090185, 0.4926829269261864, 0.5146341461476271, 0.5186991869434109, 0.5203252035427869]
val_accuracy = [0.3873239445014739, 0.3978873231041599, 0.4154929581662299, 0.42253521168735664, 0.44014084549017357, 0.4471830990113003, 0.48239436535768104, 0.49295774689862426, 0.5105633807014411, 0.5140845074620045]

fig = plt.figure(figsize=(10,10))
plt.plot(accuracy, c='blue', label='Training accuracy')
plt.plot(val_accuracy, c='red',
         label = 'Validation accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.savefig('Accuracy_Improved')
