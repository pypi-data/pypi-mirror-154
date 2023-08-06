"""Repository management for the Human Disease Ontology."""

import os
from git import Repo
from tqdm import tqdm

from . import owl, util


def restore_head_dec(function):
    def _rh_inner(self, *args, **kwargs):
        if self.head.is_detached:
            initial_head = self.head.commit
        else:
            initial_head = self.head.ref
        func = function(self, *args, **kwargs)
        self.git.checkout(initial_head)
        return func
    return _rh_inner


class DOrepo(Repo):
    """A class for the Human Disease Ontology repository."""

    def __init__(self, path):
        super().__init__(util.ensure_dir(path))
        self.path = os.path.dirname(self.git_dir)
        self._onto_dir = os.path.join(self.path, "src", "ontology")
        self.doid_edit = owl.functional(os.path.join(self._onto_dir, "doid-edit.owl"))
        self.doid = owl.xml(os.path.join(self._onto_dir, "doid.owl"))
        self.doid_merged = owl.xml(os.path.join(self._onto_dir, "doid-merged.owl"))
        self.doid_non_classified = owl.xml(os.path.join(self._onto_dir, "doid-non-classified.owl"))
        self.doid_base = owl.xml(os.path.join(self._onto_dir, "doid-base.owl"))

    @restore_head_dec
    def tag_iterate(self, fxn, which=None, *args, **kwargs):
        tags = sorted(self.tags, key=lambda t: t.commit.committed_datetime)

        val_err_msg = "`which` must be a dictionary with 'start' and 'end' elements"
        if which == None:
            tag_exec = tags
        elif isinstance(which, dict):
            if not len(which) == 2 or not set(which.keys()).issubset(['start', 'end']):
                wrong_key = set(which.keys()) - set(['start', 'end'])
                if len(wrong_key) > 0:
                    val_err_msg = val_err_msg + ", not: " + wrong_key
                raise ValueError(val_err_msg)

            for k, v in which.items():
                if not isinstance(v, str):
                    raise ValueError(
                        "which key " + k +
                        " must contain a string, not a " + type(v)
                    )

            t_name = [t.name for t in tags]
            tag_exec = tags[t_name.index(which['start']):(t_name.index(which['end']) + 1)]
        else:
            if len(which) == 0:
                raise ValueError(
                    val_err_msg +
                    ", a string/list of tag name(s), or None (for all tags)."
                )
            tag_exec = [ t for t in tags if t.name in which ]

        res = {}
        include = False
        tag_it = tqdm(tag_exec, desc="executing at...", unit="tag")
        for t in tag_it:
            self.git.checkout(t)
            res[t.name] = fxn(*args, **kwargs)

        return res

    def capture_head(self):
        if self.head.is_detached:
            self.captured_head = self.head.commit
        else:
            self.captured_head = self.head.ref
        return self.captured_head

    def restore_head(self):
        res = self.git.checkout(self.captured_head)
        return res

    def checkout_tag(self, tag_name):
        for t in self.tags:
            if t.name == tag_name:
                self.git.checkout(t)
                return t.name
        # MUST fail if tag is not found
        raise ValueError("tag_name does not correspond to any tags in the repo.")
