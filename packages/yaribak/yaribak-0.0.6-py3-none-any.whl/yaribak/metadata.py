# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import dataclasses
import json
import os

from typing import Optional


@dataclasses.dataclass
class Metadata:
  source: str
  # Time when the backup was created.
  epoch: int
  # Present if the backup was updated when called with only-if-changed.
  updated_epoch: Optional[int] = None
  # Duration after which this backup may be erased.
  min_ttl: Optional[float] = None

  def last_updated(self) -> int:
    """Unlike updated_epoch, this is not None."""
    if self.updated_epoch is not None:
      return self.updated_epoch
    return self.epoch

  def asjson(self) -> str:
    return json.dumps(dataclasses.asdict(self), indent=True, sort_keys=True)

  @staticmethod
  def fromjson(json_str: str) -> 'Metadata':
    return Metadata(**json.loads(json_str))

  def save_to(self, fname: str) -> None:
    if os.path.exists(fname):
      # Erase before writing, to ensure this is not a hardlinked file.
      os.remove(fname)
    with open(fname, 'w') as f:
      f.write(self.asjson())

  @staticmethod
  def load_from(fname: str) -> 'Metadata':
    with open(fname) as f:
      return Metadata.fromjson(f.read())
