import matplotlib.pyplot as plt
import numpy as np
import os

def plot_and_save(df, actual_col, predicted_col, output_dir='plots', filename='xgboost_plot.png'):
    """
    Creates a scatter plot of predicted vs actual values and saves it to a file.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing actual and predicted values.
        actual_col (str): Column name for actual values.
        predicted_col (str): Column name for predicted values.
        output_dir (str): Directory where the plot will be saved.
        filename (str): Filename for the saved plot.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract actual and predicted values
    y_actual = df[actual_col]
    y_predicted = df[predicted_col]
    
    # Calculate metrics
    mse = np.mean((y_actual - y_predicted) ** 2)
    r2 = 1 - (np.sum((y_actual - y_predicted) ** 2) / np.sum((y_actual - np.mean(y_actual)) ** 2))
    
    # Create the plot
    plt.figure(figsize=(10, 8))
    plt.scatter(y_actual, y_predicted, alpha=0.5)
    plt.plot([y_actual.min(), y_actual.max()], [y_actual.min(), y_actual.max()], 'r--', lw=2)
    plt.xlabel(f'Actual {actual_col}')
    plt.ylabel(f'Predicted {predicted_col}')
    plt.title(f'Actual vs Predicted {actual_col}')
    
    max_value = max(y_actual.max(), y_predicted.max())
    min_value = min(y_actual.min(), y_predicted.min())
    plt.xlim(min_value, max_value)
    plt.ylim(min_value, max_value)
    
    textstr = '\n'.join((
        f'MSE: {mse:.4f}',
        f'R-squared: {r2:.4f}'
    ))
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=9,
             verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    # Save the plot
    figure_path = os.path.join(output_dir, filename)
    plt.savefig(figure_path, dpi=300)
    print(f"Saved figure to {figure_path}")
    plt.close()



def plot_crossplot(y_true, y_pred, mse, r2, output_dir='plots', filename='xgboost_crossplot.png'):
    """
    Creates a scatter plot comparing actual vs predicted values and saves it to a file.
    
    Parameters:
        y_true (np.array or pd.Series): Actual values.
        y_pred (np.array or pd.Series): Predicted values.
        mse (float): Mean Squared Error.
        r2 (float): R-squared value.
        output_dir (str): Directory where the plot will be saved.
        filename (str): Filename for the saved plot.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the plot
    plt.figure(figsize=(10, 8))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('Actual Expected Goals')
    plt.ylabel('Predicted Expected Goals')
    plt.title('Actual vs Predicted Expected Goals')
    
    max_value = max(y_true.max(), y_pred.max())
    min_value = min(y_true.min(), y_pred.min())
    plt.xlim(min_value, max_value)
    plt.ylim(min_value, max_value)
    
    textstr = '\n'.join((
        f'MSE: {mse:.4f}',
        f'R-squared: {r2:.4f}'
    ))
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=9,
             verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    # Save the plot
    figure_path = os.path.join(output_dir, filename)
    plt.savefig(figure_path, dpi=300)
    print(f"Saved figure to {figure_path}")
    plt.close()


def plot_feature_importance(model, feature_columns, output_dir='plots', filename='xgboost_feature_importance.png'):
    """
    Creates a bar plot of feature importances from the XGBoost model and saves it to a file.
    
    Parameters:
        model (xgb.XGBModel): Trained XGBoost model.
        feature_columns (list): List of feature names.
        output_dir (str): Directory where the plot will be saved.
        filename (str): Filename for the saved plot.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get feature importance
    feature_importance = model.feature_importances_
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    
    # Create the plot
    plt.figure(figsize=(12, 12))
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, np.array(feature_columns)[sorted_idx], rotation=45)
    plt.xlabel('Feature Importance')
    plt.title('XGBoost Feature Importance')
    plt.tight_layout()
    
    # Save the plot
    figure_path = os.path.join(output_dir, filename)
    plt.savefig(figure_path, dpi=300)
    print(f"Saved figure to {figure_path}")
    plt.close()
