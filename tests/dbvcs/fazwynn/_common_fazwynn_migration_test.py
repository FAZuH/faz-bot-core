from typing import override

from tests.dbvcs.common_migration_test import CommonMigrationTest


class CommonFazdbMigrationTest:
    class Test(CommonMigrationTest.Test):
        @property
        @override
        def section_name(self) -> str:
            return "faz-wynn_test"
