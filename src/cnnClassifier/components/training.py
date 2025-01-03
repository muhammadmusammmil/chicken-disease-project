from cnnClassifier.entity.config_entity import TrainingConfig
import tensorflow as tf
from pathlib import Path

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config


    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path,
            compile=False
        )

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.params_learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def train_valid_generator(self):
        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split = 0.20
        )

        dataflow_kwargs = dict(
            target_size = tuple(self.config.params_image_size[:-1]),
            batch_size = self.config.params_batch_size,
            interpolation = 'bilinear'
        )

        valid_generator = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)

        self.valid_generator = valid_generator.flow_from_directory(
            directory=self.config.training_data,
            target_size=dataflow_kwargs['target_size'],
            batch_size=dataflow_kwargs['batch_size'],
            interpolation=dataflow_kwargs['interpolation'],
            subset="validation",
            shuffle=False
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                fill_mode='nearest',
                rescale=1./255,
                validation_split=0.20
            )
        else:
            train_datagenerator = valid_generator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            target_size=dataflow_kwargs['target_size'],
            batch_size=dataflow_kwargs['batch_size'],
            interpolation=dataflow_kwargs['interpolation'],
            subset="training",
            shuffle=True
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)


    def train(self, callback_list: list):
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            steps_per_epoch=self.steps_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator,
            callbacks=callback_list
        )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )