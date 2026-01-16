# Database Maintenance
This document provides instructions for maintaining the database used in the Indoor Climate Project. It covers tasks such as applying migrations, backing up data, and monitoring database health.

>For a more detailed guide of Alembic, refer to the official [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#).
>
>For a more detailed guide of SQLAlchemy, refer to the official [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

## Database Maintenance with SQLAlchemy
- **Create Table**:
    Open the relevant model file in `project/src/database/models.py` and define a new class that inherits from `Base`. Define the table name and columns using SQLAlchemy's ORM syntax. For example:
    ```python
    class Message(Base):
        __tablename__ = 'messages'

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String, index=True)
        content = Column(String, index=True)
        created_at = Column(DateTime, default=datetime.utcnow)
    ```
- **Modify Table**:
    To modify an existing table, update the corresponding model class in `project/src/database/models.py`. You can add new columns, change data types, or modify constraints. For example, to add a new column:
    ```python
    class Message(Base):
        __tablename__ = 'messages'

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String, index=True)
        content = Column(String, index=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        author = Column(Integer, ForeignKey('users.id'))  # New column added

        author_rel = relationship("User", back_populates="messages")  # Relationship to User model
    ```
- **Delete Table**:
    To delete a table, remove the corresponding model class from `project/src/database/models.py`. Additionally, ensure that any foreign key relationships or dependencies are handled appropriately in other models.


## Database Migrations with Alembic

1. **Generate Revision File**:
   To create a new migration script after modifying the database models, use the following command:
   ```console
   $ alembic revision --autogenerate -m "your message here"
   ```
   Replace `"your message here"` with a brief description of the changes made (e.g., "add table components", "modify column types").
2. **Review Revision File**:
    After generating a revision file, review it in the `project/migrations/versions/` directory to ensure that the changes accurately reflect the intended modifications to the database schema.

    > **Important**: When creating a new table that will handle time-series data, manually add`'op.execute("SELECT create_hypertable('<table_name>', '<time_column>', if_not_exists => TRUE);")` in the `upgrade()` function of the revision file to convert it into a hypertable. Check existing revision files for reference.
3. **Apply Migrations**:
   To apply the latest migrations to the database, run:
   ```console
   $ alembic upgrade head
   ```

## Additional Maintenance Tasks
- **Check current version**:
   To check the current version of the database schema, use:
   ```console
   $ alembic current
   ```
- **See migration history**:
   To view the history of applied migrations, run:
   ```console
   $ alembic history --verbose
   ```
- **Downgrade database**:
   To revert the database schema to a previous version, use:
   ```console
   # Downgrade by one revision
   $ alembic downgrade -1

   # Downgrade to a specific revision
   $ alembic downgrade <revision_id>
   ```
   Replace `<revision_id>` with the specific revision identifier you want to downgrade to.
- **View pending SQL commands**:
   To see the SQL commands that would be executed for an upgrade or downgrade without applying them, use:
   ```console
   # For upgrade
   $ alembic upgrade head --sql

   # For downgrade
   $ alembic downgrade -1 --sql
   ```