import hashlib
import logging
import os
import pickle
import threading
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class CacheControl:
    """Control class for LLM cache management."""

    memory: Dict[str, str] = {}
    _lock = threading.Lock()

    def __init__(self, storage_path: str = "./cache"):
        """
        Initialize the CacheControl class.

        Args:
            storage_path: Base directory for storing cache files.
        """
        self.storage_path = storage_path
        self.memory_file = os.path.join(self.storage_path, "memory.pkl")
        self._init_storage()

    def _init_storage(self) -> None:
        """Initialize the storage directory and load the memory map."""
        os.makedirs(self.storage_path, exist_ok=True)
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "rb") as f:
                    new_memory = pickle.load(f)
                    with CacheControl._lock:
                        CacheControl.memory.update(new_memory)
            except Exception as e:
                logger.error(
                    f"Failed to load memory file {self.memory_file}: {e}. Initializing empty memory."
                )

    def _save_memory_map(self) -> None:
        """Save the memory map to disk."""
        with self._lock:
            with open(self.memory_file, "wb") as f:
                pickle.dump(self.memory, f)

    def get_hash(self, kwargs: Dict[str, Any]) -> str:
        """
        Generate a SHA-256 hash for the given kwargs.

        Args:
            kwargs: The generation kwargs.

        Returns:
            A SHA-256 hash string.
        """
        copy_kwargs = kwargs.copy()

        del copy_kwargs[
            "parser"
        ]  # Remove non-deterministic model reference before hashing
        # Try to hash string representation
        data = str(copy_kwargs).encode("utf-8")

        return hashlib.sha256(data).hexdigest()

    def get_from_cache(self, kwargs: Dict[str, Any]) -> Optional[Tuple[Any, Any]]:
        """
        Load a cached response from memory using the kwargs hash.

        Args:
            kwargs: The kwargs used for generation.

        Returns:
            The cached response tuple (response, trace) if found, otherwise None.
        """

        msg_hash = self.get_hash(kwargs)

        with self._lock:
            file_path = self.memory.get(msg_hash)

        if not file_path:
            return None

        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(
                f"Error reading cache file {file_path}: {e} for hash {msg_hash}"
            )
            return None

    def save_to_cache(self, kwargs: Dict[str, Any], result) -> None:
        """
        Save a response to cache.

        Args:
            kwargs: The kwargs used for generation.
            result: The result to cache (response, trace).
        """
        msg_hash = self.get_hash(kwargs)
        file_path = os.path.join(self.storage_path, f"{msg_hash}.pkl")

        try:
            with open(file_path, "wb") as f:
                pickle.dump(result, f)

            with self._lock:
                self.memory[msg_hash] = file_path

            self._save_memory_map()
        except Exception as e:
            logger.error(f"Error saving to cache file {file_path}: {e}")
