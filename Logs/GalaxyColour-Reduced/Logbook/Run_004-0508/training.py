import matplotlib.pyplot as plt

accuracy = [0.5630081301782189, 0.5630081301782189, 0.5630081297905465, 0.5630081303720552, 0.5630081297905465, 0.5630081299843827, 0.5630081299359236, 0.5630081298874645, 0.5630081301782189, 0.5630081301782189]
val_accuracy =  [0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529, 0.6197183090196529]


fig = plt.figure(figsize=(10,10))
plt.plot(accuracy, c='blue', label='Training accuracy')
plt.plot(val_accuracy, c='red',
         label = 'Validation accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.savefig('CentralVsSatellite_Reduced_Accuracy')

