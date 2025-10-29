# Reminder to Add Crontab Entry

To ensure the `run_update_activation_state.sh` script runs every minute, follow these steps:

1. Open the crontab editor:
    ```sh
    crontab -e
    ```

2. Add the following line to the crontab file (You might need to update the file path):
    ```sh
    * * * * * /wildops_project/WildOpsProject/scripts/run_update_activation_state.sh
    ```

3. Save and exit the editor.

This will schedule the script to run every minute.