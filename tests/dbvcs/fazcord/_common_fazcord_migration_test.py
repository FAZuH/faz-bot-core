from typing import override

from tests.dbvcs.common_migration_test import CommonMigrationTest


class CommonFazcordMigrationTest:
    class Test(CommonMigrationTest.Test):

        @property
        @override
        def db_name(self) -> str:
            return "faz-cord_test"
