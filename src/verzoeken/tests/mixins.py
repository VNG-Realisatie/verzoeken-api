from unittest.mock import patch


class VerzoekInformatieObjectSyncMixin:
    def setUp(self):
        super().setUp()

        patcher_sync_create = patch("verzoeken.sync.signals.sync_create_vio")
        self.mocked_sync_create_vio = patcher_sync_create.start()
        self.addCleanup(patcher_sync_create.stop)

        patcher_sync_delete = patch("verzoeken.sync.signals.sync_delete_vio")
        self.mocked_sync_delete_vio = patcher_sync_delete.start()
        self.addCleanup(patcher_sync_delete.stop)
