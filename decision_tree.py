"""
Predict the likelihood of a household to purchase a solar panel
"""
import pandas as pd
import chardet
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    # Path to the CSV file
    path_data = "data/inputs/nexigoSolar.csv"

    # show plots
    show_plots = True

    # Detect the encoding of the CSV file
    with open(path_data, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")

    # Import the CSV file
    all_addresses = pd.read_csv(
        path_data, on_bad_lines='skip',
        sep=',', decimal=',', encoding=encoding)

    # Show the column names
    print(all_addresses.columns)

    # how many rows are there?
    print(f"Number of rows: {len(all_addresses)}")

    # type of house based on lcgchar
    # if lcgchar in [1, 2, 7, 9] its 1 else 0
    all_addresses['house'] = \
        np.where(all_addresses['lcgchar'].isin([1, 2, 7, 9]), 1, 0)

    # if date_solar is not null, then set the value to 1, else 0
    all_addresses['target'] = \
        np.where(all_addresses['date_solar'].notna(), 1, 0)

    # print the share of houses with solar panels
    print("Share of houses with solar panels:")
    print(all_addresses['target'].mean())
    print("\n")

    # only keep the relevant columns
    # high income = kk_mio or kk_idx
    # house or appartment = lcgchar
    # proxy for education = lcschicht
    # affinity environment = lceemob
    # likelihood to change heating = lcewb
    # age of the house = lcbjkl
    model_data = \
        all_addresses[
            ['house', 'kk_mio',
            'lcgchar', 'lcschicht', 'lceemob',
            'lcewb', 'lcbjkl', 'target']
            ]

    # plot the correlation matrix with the target
    if show_plots:
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            model_data.corr(), annot=True, fmt='.2f', cmap='coolwarm',
            # y label only the target
            xticklabels=model_data.columns, yticklabels=model_data.columns)
        plt.title('Correlation Matrix')
        plt.savefig("img/correlation_matrix.png")
        plt.show()

    # X is everything except the target column
    # y is the target column
    X = model_data.drop(columns=['target'])
    y = model_data.target

    # split into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # add a sample weight
    weight = \
        np.where(y_train == 1, 1, 0.5)

    # which tree?
    classification_tree = False
    use_weight = False

    # Create and train classification tree
    if classification_tree:
        print("Training classification tree...")
        clf = DecisionTreeClassifier(random_state=42, max_depth=6, min_samples_split=100)
        if use_weight:
            clf.fit(X_train, y_train, sample_weight=weight)
        else:
            clf.fit(X_train, y_train)
        print("Training complete.")

        # validate the model
        print("Validating model...")
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Model validated.")

        # add the predictions to the whole dataset
        all_addresses['predictions'] = clf.predict(X)

        # print the share of houses with solar panels based on the predictions
        print("Share of houses with solar panels based on the predictions:")
        print(all_addresses['predictions'].mean())
        print("\n")

        # export the predictions to a csv file
        all_addresses.to_csv("data/results/dt_solar.csv", index=False, sep=';', decimal=',')

        # plot the tree
        if show_plots:
            print("Plotting tree...")
            plt.figure(figsize=(20, 10))
            plot_tree(clf, filled=True, feature_names=X.columns, class_names=['no', 'yes'])
            plt.savefig("img/decision_tree.png")
            plt.show()
            print("Tree plotted.")
    else:
        # Create and train regression tree
        print("Training regression tree...")
        clf = DecisionTreeRegressor(random_state=42, max_depth=6, min_samples_split=100)
        if use_weight:
            clf.fit(X_train, y_train, sample_weight=weight)
        else:
            clf.fit(X_train, y_train)
        print("Training complete.")

        # add the predictions to the whole dataset
        all_addresses['predictions'] = clf.predict(X)

        # print the share of houses with solar panels based on the predictions
        print("Share of houses with solar panels based on the predictions:")
        print(all_addresses['predictions'].mean())
        print("\n")

        # validate the model
        print("Validating model...")
        y_pred = clf.predict(X_test)
        # convert the predictions to binary
        y_pred = np.where(y_pred > 0.5, 1, 0)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Model validated.")

        # print a confusion matrix
        if show_plots:
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['no', 'yes'], yticklabels=['no', 'yes'])
            plt.xlabel('Predicted')
            plt.ylabel('True')
            plt.title('Confusion Matrix')
            plt.show()

            # plot the distribution of the predictions
            plt.figure(figsize=(10, 5))
            sns.histplot(all_addresses['predictions'], bins=50, kde=True)
            plt.xlabel('Predictions')
            plt.ylabel('Frequency')
            plt.title('Distribution of Predictions')
            plt.show()

        # export the predictions to a csv file
        all_addresses.to_csv("data/results/rt_solar.csv", index=False, sep=';', decimal=',', encoding=encoding)

