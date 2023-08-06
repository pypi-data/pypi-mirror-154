import os
import re
import fileseq
from collections import defaultdict
from kabaret import flow
from kabaret.flow_entities.entities import Entity, Property
from libreflow.utils.kabaret.flow_entities.entities import EntityView
from libreflow.baseflow.maputils import SimpleCreateAction
from libreflow.baseflow.film import Film as BaseFilm
from libreflow.baseflow.shot import Sequence as BaseSequence, Shot as BaseShot, ShotCollection
from libreflow.baseflow.task import TaskCollection
from libreflow.baseflow.file import CreateDefaultFilesAction, GenericRunAction
from libreflow.baseflow.users import ToggleBookmarkAction

from .packaging import PackAction, CreateLayoutPackagesAction, CreateCleanPackagesAction
from .unpacking import UnpackCleanPackagesAction, UnpackLayoutPackagesAction
from .export import RequestFilesAction
from .compositing import InitCompScene
from .shotgrid import ShotGridEntity

from libreflow.resources.icons import libreflow as _, applications as _
from ..resources.icons import gui as _


MAX_DELIVERY_COUNT = 1e3


class CompRevisionsMultiChoiceValue(flow.values.MultiChoiceValue):

    _shot = flow.Parent(2)

    def __init__(self, parent, name):
        super(CompRevisionsMultiChoiceValue, self).__init__(parent, name)
        self._file = None
        if self._shot.tasks['compositing'].files.has_mapped_name('compositing_movie_mov'):
            self._file = self._shot.tasks['compositing'].files['compositing_movie_mov']

    def choices(self):
        if self._file is not None:
            return sorted(self._file.get_revision_names(sync_status='Available', published_only=True), reverse=True)
        else:
            return ''

    def revert_to_default(self):
        if self._file is None or self._file.is_empty():
            self.set('')
            return

        revision = self._file.get_head_revision(sync_status='Available')
        revision_name = ''
        
        if revision is None:
            choices = self.choices()
            if choices:
                revision_name = choices[0]
        else:
            revision_name = revision.name()
        
        self.set(revision_name)
    
    def _fill_ui(self, ui):
        super(CompRevisionsMultiChoiceValue, self)._fill_ui(ui)
        if self._file is None or self._file.is_empty(on_current_site=True):
            ui['hidden'] = True


class AnimaticRevisionsMultiChoiceValue(CompRevisionsMultiChoiceValue):

    _shot = flow.Parent(2)

    def __init__(self, parent, name):
        super(AnimaticRevisionsMultiChoiceValue, self).__init__(parent, name)
        self._file = None
        if self._shot.tasks['misc'].files.has_mapped_name('animatic_mp4'):
            self._file = self._shot.tasks['misc'].files['animatic_mp4']
    
    def revert_to_default(self):
        self.set([])


class CreateDepartmentDefaultFilesAction(CreateDefaultFilesAction):

    _department = flow.Parent()

    def get_target_groups(self):
        return [self._department.name()]

    def get_file_map(self):
        return self._department.files


class AbstractRVOption(GenericRunAction):
    """
    Abstract run action which instantiate an RV runner,
    with its default version.
    """
    def runner_name_and_tags(self):
        return 'RV', []
    
    def get_version(self, button):
        return None


class CompareWithAnimaticAction(AbstractRVOption):
    """
    Compares a shot compositing preview with its animatic,
    if both files.
    """
    ICON = ('icons.libreflow', 'compare-previews')

    _comp_preview_path  = flow.Computed(cached=True)
    _animatic_path = flow.Computed(cached=True)

    _shot = flow.Parent()

    def needs_dialog(self):
        self._comp_preview_path.touch()
        self._animatic_path.touch()

        return (
            self._comp_preview_path.get() is None
            or self._animatic_path.get() is None
        )
    
    def get_buttons(self):
        if self._comp_preview_path.get() is None:
            self.message.set('<h2>This shot has no compositing preview.</h2>')
        elif self._animatic_path.get() is None:
            self.message.set('<h2>This shot has no animatic.</h2>')
        
        return ['Close']

    def compute_child_value(self, child_value):
        if child_value is self._animatic_path:
            self._animatic_path.set(
                self._get_last_revision_path('misc', 'animatic.mp4')
            )
        elif child_value is self._comp_preview_path:
            self._comp_preview_path.set(
                self._get_last_revision_path('compositing', 'compositing_movie.mov')
            )
    
    def extra_argv(self):
        return [
            '-wipe', '-autoRetime', '0',
            self._comp_preview_path.get(),
            self._animatic_path.get()
        ]

    def run(self, button):
        if button == 'Close':
            return
        else:
            super(CompareWithAnimaticAction, self).run(button)

    def _get_last_revision_path(self, task_name, file_name):
        path = None

        if self._shot.tasks.has_mapped_name(task_name):
            task = self._shot.tasks[task_name]
            name, ext = file_name.rsplit('.', 1)

            if task.files.has_file(name, ext):
                f = task.files[f'{name}_{ext}']
                r = f.get_head_revision()

                if r is not None and r.get_sync_status() == "Available":
                    path = r.get_path()

        return path


class CompareCompMovies(flow.Action):
    
    ICON = ('icons.libreflow', 'compare-previews')

    _shot = flow.Parent()
    revisions = flow.Param([], CompRevisionsMultiChoiceValue).ui(label="Comp Revisions")
    antc_revisions = flow.Param([], AnimaticRevisionsMultiChoiceValue).ui(label="Animatic Revisions")

    def __init__(self, parent, name):
        super(CompareCompMovies, self).__init__(parent, name)
        self._file = None
        if self._shot.tasks['compositing'].files.has_mapped_name('compositing_movie_mov'):
            self._file = self._shot.tasks['compositing'].files['compositing_movie_mov']

    def needs_dialog(self):
        return True
    
    def get_buttons(self):
        if self._file is None:
            self.message.set('<h3>This shot has no comp movies</h3>')
            return ['Cancel']
        elif self._file.is_empty() == True or len(self._file.get_revision_names(sync_status='Available', published_only=True)) == 0:
            self.message.set('<h3>This shot has no comp revision</h3>')
            return ['Cancel']
        elif len(self._file.get_revision_names(sync_status='Available', published_only=True)) < 2:
            self.message.set('<h3>This shot has only one comp revision</h3>')
            return ['Cancel']
        else:
            self.message.set('<h3>Choose revisions to compare</h3>')
            self.revisions.set([self.revisions.choices()[0], self.revisions.choices()[1]])
            self.antc_revisions.revert_to_default()
            return ['Open', 'Cancel']

    def run(self, button):
        if button == "Cancel":
            return
        
        self._file.compare_rv.revisions.set(self.revisions.get())
        self._file.compare_rv.antc_revisions.set(self.antc_revisions.get())

        return self.get_result(goto_target=self._file.compare_rv.run('Open'))


class LastFilesTypeChoiceValue(flow.values.ChoiceValue):

    CHOICES = ['Animation Layers', 'Background', 'Comp', 'Sources']
    CHOICES_ICONS = {
        "Animation Layers": ('icons.gui', 'anim-layers'),
        "Background": ('icons.flow', 'photoshop'),
        "Comp": ('icons.libreflow', 'afterfx'),
        "Sources": ('icons.gui', 'open-folder')
    }

    def choices(self):
        return self.CHOICES
    
    def revert_to_default(self):
        default_value = self.CHOICES[0]
        self.set(default_value)
    
    def _fill_ui(self, ui):
        super(LastFilesTypeChoiceValue, self)._fill_ui(ui)
        ui['icon'] = ('icons.gui', 'file')


class OpenLastFiles(GenericRunAction):

    ICON = ('icons.gui', 'file')

    file_type = flow.Param('', LastFilesTypeChoiceValue).ui(choice_icons=LastFilesTypeChoiceValue.CHOICES_ICONS)

    _layers_paths     = flow.Computed(cached=True)
    _background_path  = flow.Computed(cached=True)
    _comp_path        = flow.Computed(cached=True)
    _sources_path     = flow.Computed(cached=True)

    _shot = flow.Parent()

    def needs_dialog(self):
        self._layers_paths.touch()
        self._background_path.touch()
        self._comp_path.touch()
        self._sources_path.touch()

        return (
            not bool(self._layers_paths.get()),
            self._background_path.get() is None,
            self._comp_path.get() is None,
            self._sources_path.get() is None
        )
    
    def compute_child_value(self, child_value):
        if child_value is self._layers_paths:
            self._layers_paths.set(self._get_layers_paths())

        elif child_value is self._background_path:
            self._background_path.set(
                self._get_last_revision_path('misc', 'background.psd')
            )

        elif child_value is self._comp_path:
            self._comp_path.set(
                self._get_last_revision_path('compositing', 'compositing.aep')
            )

        elif child_value is self._sources_path:
            self._sources_path.set(
                self._get_last_revision_path('misc', 'sources')
            )

    def get_buttons(self):
        self.file_type.revert_to_default()
        return ['Select', 'Cancel']

    def runner_name_and_tags(self):
        if self.file_type.get() == "Animation Layers":
            return "RV", []
        else:
            return "DefaultEditor", []
    
    def get_version(self, button):
        return None
    
    def extra_argv(self):
        if self.file_type.get() == "Animation Layers":
            paths = []
            for col_path, line_path in self._layers_paths.get():
                if line_path is not None:
                    paths.append(line_path)
                if col_path is not None:
                    paths.append(col_path)
            return ['-bg', 'checker', '-over'] + paths

        elif self.file_type.get() == "Background":
            return [self._background_path.get()]

        elif self.file_type.get() == "Comp":
            return [self._comp_path.get()]

        elif self.file_type.get() == "Sources":
            return [self._sources_path.get()]
    
    def run(self, button):
        if button == 'Cancel':
            return

        if self.file_type.get() == "Animation Layers" and self._layers_paths.get() == []:
            self.message.set('This shot has no animation layers.')
            return self.get_result(close=False)

        if self.file_type.get() == "Background" and self._background_path.get() == None:
            self.message.set('This shot has no background file.')
            return self.get_result(close=False)

        if self.file_type.get() == "Comp" and self._comp_path.get() == None:
            self.message.set('This shot has no compositing file.')
            return self.get_result(close=False)

        if self.file_type.get() == "Sources" and self._comp_path.get() == None:
            self.message.set('This shot has no sources folder available on current site.')
            return self.get_result(close=False)
        
        super(OpenLastFiles, self).run(button)

    def _get_last_revision_path(self, task_name, file_name):
        path = None

        if self._shot.tasks.has_mapped_name(task_name):
            task = self._shot.tasks[task_name]

            if file_name == "sources":
                r = None
                if task.files.has_folder(file_name):
                    f = task.files[file_name]
                    r = f.get_head_revision()
            else:
                name, ext = file_name.rsplit('.', 1)
                r = None
                if task.files.has_file(name, ext):
                    f = task.files[f'{name}_{ext}']
                    r = f.get_head_revision()

            if r is not None and r.get_sync_status() == "Available":
                path = r.get_path()

        return path
    
    def _get_layers_paths(self):
        paths = {}

        if self._shot.tasks.has_mapped_name('clean'):
            clean = self._shot.tasks['clean']

            if clean.files.has_folder('layers'):
                f = clean.files['layers']
                r = f.get_head_revision()

                if r is not None:
                    layers_folder = r.get_path()

                    paths = defaultdict(lambda: [None, None])
                    for dir_name in os.listdir(layers_folder):
                        dir_path = os.path.join(layers_folder, dir_name)
                        m = re.match('(.*)_(col|color)$', dir_name, re.IGNORECASE)
                        index = 0
                        if m is None:
                            m = re.match('(.*)_(line)$', dir_name, re.IGNORECASE)
                            index = 1
                            if m is None:
                                continue
                        
                        sequences = fileseq.findSequencesOnDisk(dir_path)
                        if sequences:
                            seq_format = sequences[0].format(template='{basename}{padding}{extension}')
                            paths[m.group(1)][index] = os.path.join(dir_path, seq_format)

        return sorted(paths.values())


class Shot(BaseShot, ShotGridEntity):

    tasks = flow.Child(TaskCollection).ui(expanded=True)

    compare_comp_antc    = flow.Child(CompareWithAnimaticAction).ui(
        label='Compare with animatic'
    )
    compare_comp_movies  = flow.Child(CompareCompMovies).ui(
        label="Compare comp movies"
    )
    open_last_files      = flow.Child(OpenLastFiles).ui(
        label='Open last files'
    )

    def ensure_tasks(self):
        """
        Creates the tasks of this shot based on the task
        templates of the project, skipping any existing task.
        """
        mgr = self.root().project().get_task_manager()

        for dt in mgr.default_tasks.mapped_items():
            if not self.tasks.has_mapped_name(dt.name()) and not dt.optional.get():
                t = self.tasks.add(dt.name())
                t.enabled.set(dt.enabled.get())
        
        self.tasks.touch()


class Shots(ShotCollection):

    def add(self, name, object_type=None):
        """
        Adds a shot to the global shot collection, and creates
        its tasks.
        """
        s = super(Shots, self).add(name, object_type)
        s.ensure_tasks()

        return s


class CreateSGShots(flow.Action):

    ICON = ('icons.flow', 'shotgrid')

    skip_existing = flow.SessionParam(False).ui(editor='bool')

    _sequence = flow.Parent()

    def get_buttons(self):
        return ['Create shots', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        skip_existing = self.skip_existing.get()
        shots_data = self.root().project().get_shotgrid_config().get_shots_data(
            self._sequence.shotgrid_id.get()
        )
        for data in shots_data:
            name = data['name'].lower()

            if not self._sequence.shots.has_mapped_name(name):
                s = self._sequence.shots.add(name)
            elif not skip_existing:
                s = self._sequence.shots[name]
            else:
                continue
            
            print(f'Create shot {self._sequence.name()} {data["name"]}')
            s.shotgrid_id.set(data['shotgrid_id'])
        
        self._sequence.shots.touch()


class Sequence(BaseSequence, ShotGridEntity):

    shots = flow.Child(Shots).ui(expanded=True)

    with flow.group('ShotGrid'):
        create_shots = flow.Child(CreateSGShots)


class CreateSGSequences(flow.Action):

    ICON = ('icons.flow', 'shotgrid')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    create_shots = flow.SessionParam(False).ui(editor='bool')

    _film = flow.Parent()

    def get_buttons(self):
        return ['Create sequences', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        sequences_data = self.root().project().get_shotgrid_config().get_sequences_data()
        create_shots = self.create_shots.get()
        skip_existing = self.skip_existing.get()

        for data in sequences_data:
            name = data['name'].lower()

            if not self._film.sequences.has_mapped_name(name):
                s = self._film.sequences.add(name)
            elif not skip_existing:
                s = self._film.sequences[name]
            else:
                continue
            
            print(f'Create sequence {data["name"]}')
            s.shotgrid_id.set(data['shotgrid_id'])

            if create_shots:
                s.create_shots.skip_existing.set(skip_existing)
                s.create_shots.run('Create shots')
        
        self._film.sequences.touch()


class PackageTypeChoiceValue(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'
    CHOICES = ['Layout', 'Clean']

    _action = flow.Parent()

    def choices(self):
        return self.CHOICES
    
    def revert_to_default(self):
        values = self.root().project().get_action_value_store().get_action_values(
            self._action.name(), {self.name(): self.get()}
        )
        value = values[self.name()]

        if value in self.choices():
            self.set(value)


class CreatePackagesAction(flow.Action):

    ICON = ('icons.gui', 'package')

    package_type = flow.SessionParam('Layout', PackageTypeChoiceValue)

    _film = flow.Parent()

    def get_buttons(self):
        self.package_type.revert_to_default()
        return ['Select', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        if self.package_type.get() == 'Layout':
            ret = self.get_result(
                next_action=self._film.create_layout_packages.oid()
            )
        else:
            ret = self.get_result(
                next_action=self._film.create_clean_packages.oid()
            )
        
        return ret


class UnpackPackagesAction(flow.Action):

    ICON = ('icons.gui', 'package')

    package_type = flow.SessionParam('Layout', PackageTypeChoiceValue)

    _film = flow.Parent()

    def get_buttons(self):
        self.package_type.revert_to_default()
        return ['Select', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        if self.package_type.get() == 'Layout':
            ret = self.get_result(
                next_action=self._film.unpack_layout_packages.oid()
            )
        else:
            ret = self.get_result(
                next_action=self._film.unpack_clean_packages.oid()
            )
        
        return ret


class RequestAnimLayersAction(RequestFilesAction):

    ICON = ('icons.gui', 'anim-layers')


class Film(BaseFilm):

    with flow.group('Packages'):
        create_packages        = flow.Child(CreatePackagesAction).ui(label='Create')
        create_layout_packages = flow.Child(CreateLayoutPackagesAction)
        create_clean_packages  = flow.Child(CreateCleanPackagesAction)
        unpack_packages        = flow.Child(UnpackPackagesAction).ui(label='Unpack')
        unpack_layout_packages = flow.Child(UnpackLayoutPackagesAction)
        unpack_clean_packages  = flow.Child(UnpackCleanPackagesAction)
    with flow.group('Request'):
        request_layers         = flow.Child(RequestAnimLayersAction).ui(label='Layers')
    with flow.group('ShotGrid'):
        create_sequences       = flow.Child(CreateSGSequences)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(film=self.name())

    def _fill_ui(self, ui):
        if self.root().project().show_login_page():
            ui['custom_page'] = 'libreflow.baseflow.LoginPageWidget'
