import json
import os
import tensorflow as tf
import constants
from ultralytics import YOLO

# Define a function for decaying the learning rate.
# You can define any decay function you need.
# def decay(epoch):
#     if epoch < 3:
#         return 1e-3
#     elif epoch >= 3 and epoch < 7:
#         return 1e-4
#     else:
#         return 1e-5


def main():
    # MultiWorkerMirroredStrategy creates copies of all variables in the model's
    # layers on each device across all workers
    communication_options = tf.distribute.experimental.CommunicationOptions(
        implementation=tf.distribute.experimental.CollectiveCommunication.AUTO
    )
    strategy = tf.distribute.MultiWorkerMirroredStrategy(
        communication_options=communication_options
    )
    print("Number of devices: {}".format(strategy.num_replicas_in_sync))

    # Calculate the number of instancts in a batch over all workers (replicas)
    buffer_size = constants.BUFFER_SIZE
    batch_size = constants.BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync

    with strategy.scope():
        # Create train and eval datasets. For distributed training,
        # we don't use the eval dataset for now
        #train_dataset, eval_dataset = create_datasets(buffer_size, batch_size)
        # We want to shard our training data across all workers,
        # each of the workers will read the entire dataset and
        # only process the shard assigned to it.
        # All other shards will be discarded.
        # https://www.tensorflow.org/tutorials/distribute/input#sharding
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = (
            tf.data.experimental.AutoShardPolicy.DATA
        )
        # train_dataset = train_dataset.with_options(options)
        # # Declare our model
        # model = build_model()

    # Define some callbacks
    # Printing the learning rate at the end of each epoch.
    # class PrintLR(tf.keras.callbacks.Callback):
    #     def on_epoch_end(self, epoch, logs=None):
    #         print(
    #             "\nLearning rate for epoch {} is {}".format(
    #                 epoch + 1, model.optimizer.lr.numpy()
    #             )
    #         )

    # Parse environment variable TF_CONFIG to get
    # job_name and task_index
    # Here is an example of tf_config
    tf_config = {
        'cluster': {
            'worker': ['localhost:12345', 'localhost:23456']
        },
        'task': {'type': 'worker', 'index': 0}
    }
    tf_config = json.loads(os.environ.get("TF_CONFIG") or "{}")
    print("tf_config:")
    print(tf_config)
    task_config = tf_config.get("task", {})
    task_index = task_config.get("index")

    # # Define the checkpoints
    # checkpoint_prefix = os.path.join(constants.CKPT_DIR, "ckpt_{epoch}")

    # Fit the model
    # callbacks = [
    #     tf.keras.callbacks.TensorBoard(log_dir="./logs"),
    #     tf.keras.callbacks.ModelCheckpoint(
    #         filepath=checkpoint_prefix, save_weights_only=True
    #     ),
    #     tf.keras.callbacks.LearningRateScheduler(decay),
    #     PrintLR(),
    # ]

    # model.fit(train_dataset, epochs=constants.NUM_EPOCHS, callbacks=callbacks)
    model = YOLO("yolov8n.pt")
    model.train(data="/dataset.yaml", epochs=10)


    # If the worker is a chief, save the model to it,
    # otherwise, save to all of the workers
    if task_index == 0:
        saved_model_dir = constants.SAVED_MODEL_DIR
    else:
        saved_model_dir = f"{constants.SAVED_MODEL_DIR}/workertemp_{task_index}"

    # Save the model
    print(f"Saving model to {saved_model_dir}")
    model.save(saved_model_dir)


if __name__ == "__main__":
    main()