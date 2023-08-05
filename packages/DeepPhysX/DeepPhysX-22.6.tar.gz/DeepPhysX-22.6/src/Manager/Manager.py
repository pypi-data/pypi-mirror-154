from typing import Any, Dict, Tuple, Optional
from os.path import join as osPathJoin
from os.path import isfile, basename, exists
from datetime import datetime
from numpy import ndarray

from DeepPhysX.Core.Manager.DataManager import DataManager
from DeepPhysX.Core.Manager.NetworkManager import NetworkManager
from DeepPhysX.Core.Manager.StatsManager import StatsManager
from DeepPhysX.Core.Environment.BaseEnvironmentConfig import BaseEnvironmentConfig
from DeepPhysX.Core.Dataset.BaseDatasetConfig import BaseDatasetConfig
from DeepPhysX.Core.Network.BaseNetworkConfig import BaseNetworkConfig
from DeepPhysX.Core.Utils.pathUtils import get_first_caller, create_dir


class Manager:
    """
    | Collection of all the specialized managers. Allows for some basic functions call.
    | More specific behaviour have to be directly call from the corresponding manager.

    :param BasePipeline pipeline: Specialisation That define the type of usage
    :param Optional[BaseNetworkConfig] network_config: Specialisation containing the parameters of the network manager
    :param Optional[BaseDatasetConfig] dataset_config: Specialisation containing the parameters of the dataset manager
    :param Optional[BaseEnvironmentConfig] environment_config: Specialisation containing the parameters of the
                                                               environment manager
    :param str session_name: Name of the newly created directory if session_dir is not defined
    :param str session_dir: Name of the directory in which to write all of the necessary data
    :param bool new_session: Define the creation of new directories to store data
    :param int batch_size: Number of samples in a batch
    """

    def __init__(self,
                 pipeline: Optional[Any] = None,
                 network_config: Optional[BaseNetworkConfig] = None,
                 dataset_config: Optional[BaseDatasetConfig] = None,
                 environment_config: Optional[BaseEnvironmentConfig] = None,
                 session_name: str = 'default',
                 session_dir: str = None,
                 new_session: bool = True,
                 batch_size: int = 1):

        self.pipeline: Any = pipeline
        #Constructing the session_dir with the provided arguments
        if session_name is None:
            raise ValueError("[Manager] The session name cannot be set to None (will raise error).")
        if session_dir is None:
            # Create manager directory from the session name
            self.session_dir: str = osPathJoin(get_first_caller(), session_name)
        else:
            self.session_dir: str = osPathJoin(session_dir, session_name)

        # Trainer: must create a new session to avoid overwriting
        if pipeline.type == 'training':
            train = True
            # Avoid unwanted overwritten data
            if new_session:
                self.session_dir: str = create_dir(self.session_dir, dir_name=session_name)
        # Prediction: work in an existing session
        elif pipeline.type == 'prediction':
            train = False
            if not exists(self.session_dir):
                raise ValueError("[Manager] The session directory {} does not exists.".format(self.session_dir))
        else:
            raise ValueError("[Manager] The pipeline must be either training or prediction.")

        self.session_name: str = session_name
        # Always create the NetworkMmanager
        self.network_manager = NetworkManager(manager=self,
                                              network_config=network_config,
                                              session_name=self.session_name,
                                              session_dir=self.session_dir,
                                              new_session=new_session,
                                              train=train)
        # Always create the DataManager for same reason
        self.data_manager = DataManager(manager=self,
                                        dataset_config=dataset_config,
                                        environment_config=environment_config,
                                        session_name=self.session_name,
                                        session_dir=self.session_dir,
                                        new_session=new_session,
                                        training=train,
                                        record_data=pipeline.record_data,
                                        batch_size=batch_size)
        # Create the StatsManager for training
        self.stats_manager = StatsManager(manager=self,
                                          log_dir=osPathJoin(self.session_dir, 'stats/')) if train else None

    def get_pipeline(self) -> Any:
        """
        | Return the pipeline that is using the Manager.

        :return: Pipeline that uses the manager
        """

        return self.pipeline

    def get_data(self, epoch: int = 0, batch_size: int = 1, animate: bool = True) -> None:
        """
        | Fetch data from the DataManager.

        :param int epoch: Epoch ID
        :param int batch_size: Size of a batch
        :param bool animate: If True allows running environment step
        """

        self.data_manager.get_data(epoch=epoch, batch_size=batch_size, animate=animate)

    def optimize_network(self) -> Tuple[ndarray, Dict[str, float]]:
        """
        | Compute a prediction and run a back propagation with the current batch.

        :return: The network prediction and the associated loss value
        """

        # Normalize input and output data
        data = self.data_manager.data
        for field in ['input', 'output']:
            if field in data:
                data[field] = self.data_manager.normalize_data(data[field], field)
        # Forward pass and optimization step
        prediction, loss_dict = self.network_manager.compute_prediction_and_loss(data, optimize=True)
        return prediction, loss_dict

    def set_eval(self) -> None:
        self.network_manager.set_eval()
        self.data_manager.set_eval()

    def set_train(self) -> None:
        self.network_manager.set_train()
        self.data_manager.set_train()

    def save_network(self) -> None:
        """
        | Save network weights as a pth file
        """

        self.network_manager.save_network()

    def close(self) -> None:
        """
        | Call all managers close procedure
        """

        if self.network_manager is not None:
            self.network_manager.close()
        if self.stats_manager is not None:
            self.stats_manager.close()
        if self.data_manager is not None:
            self.data_manager.close()

    def save_info_file(self) -> None:
        """
        | Called by the Trainer to save a .txt file which provides a quick description template to the user and lists
          the description of all the components.
        """

        filename = osPathJoin(self.session_dir, 'infos.txt')
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not isfile(filename):
            f = open(filename, "w+")
            # Session description template for user
            f.write("## DeepPhysX Training Session ##\n")
            f.write(date_time + "\n\n")
            f.write("Purpose of the training session:\nNetwork Input:\nNetwork Output:\nComments:\n\n")
            # Listing every component descriptions
            f.write("## List of Components Parameters ##\n")
            f.write(str(self.pipeline))
            f.write(str(self))
            f.close()

    def __str__(self) -> str:
        """
        :return: A string containing valuable information about the Managers
        """

        manager_description = ""
        if self.network_manager is not None:
            manager_description += str(self.network_manager)
        if self.data_manager is not None:
            manager_description += str(self.data_manager)
        if self.stats_manager is not None:
            manager_description += str(self.stats_manager)
        return manager_description
