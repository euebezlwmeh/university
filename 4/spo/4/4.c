#include <sqlite3.h>
#include <gtk/gtk.h>
#include <stdio.h>
#include <string.h>

sqlite3 *db;
GtkWidget *window;
GtkWidget *notebook;
GtkWidget *status_label;

typedef struct {
    GtkWidget *treeview;
    GtkListStore *store;
    char *table_name;
} TableData;

void execute_sql(const char *sql, char **errmsg) {
    if (sqlite3_exec(db, sql, NULL, NULL, errmsg) != SQLITE_OK) {
        gtk_label_set_text(GTK_LABEL(status_label), *errmsg);
        sqlite3_free(*errmsg);
    }
}

void refresh_table_view(TableData *data) {
    GtkTreeIter iter;
    char **result;
    int rows, cols;
    char *errmsg = NULL;
    char sql[256];

    gtk_list_store_clear(data->store);

    snprintf(sql, sizeof(sql), "SELECT * FROM %s", data->table_name);

    if (sqlite3_get_table(db, sql, &result, &rows, &cols, &errmsg) != SQLITE_OK) {
        gtk_label_set_text(GTK_LABEL(status_label), errmsg);
        sqlite3_free(errmsg);
        return;
    }

    for (int i = 1; i <= rows; i++) {
        gtk_list_store_append(data->store, &iter);
        for (int j = 0; j < cols; j++) {
            gtk_list_store_set(data->store, &iter, j, result[i * cols + j], -1);
        }
    }
    
    sqlite3_free_table(result);
}

void on_add_button_clicked(GtkButton *button, TableData *data) {
    GtkWidget *dialog, *content_area, *grid, *entry;
    GtkDialogFlags flags = GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT;
    int response;
    char sql[512];
    char *errmsg = NULL;

    dialog = gtk_dialog_new_with_buttons("Добавить запись", 
                                        GTK_WINDOW(window),
                                        flags,
                                        "Добавить",
                                        GTK_RESPONSE_ACCEPT,
                                        "Отмена",
                                        GTK_RESPONSE_REJECT,
                                        NULL);
    
    content_area = gtk_dialog_get_content_area(GTK_DIALOG(dialog));
    grid = gtk_grid_new();
    gtk_container_add(GTK_CONTAINER(content_area), grid);

    char **result;
    int rows, cols;
    snprintf(sql, sizeof(sql), "PRAGMA table_info(%s)", data->table_name);
    sqlite3_get_table(db, sql, &result, &rows, &cols, &errmsg);
    
    GtkWidget *entries[rows];

    for (int i = 1; i <= rows; i++) {
        const char *col_name = result[i * cols + 1];
        
        if (strcmp(col_name, "id") == 0) continue;
        
        GtkWidget *label = gtk_label_new(col_name);
        entry = gtk_entry_new();
        entries[i-1] = entry;
        
        gtk_grid_attach(GTK_GRID(grid), label, 0, i-1, 1, 1);
        gtk_grid_attach(GTK_GRID(grid), entry, 1, i-1, 1, 1);
    }
    
    gtk_widget_show_all(dialog);
    response = gtk_dialog_run(GTK_DIALOG(dialog));
    
    if (response == GTK_RESPONSE_ACCEPT) {
        char columns[256] = "";
        char values[256] = "";
        int first = 1;
        
        for (int i = 1; i <= rows; i++) {
            const char *col_name = result[i * cols + 1];
            if (strcmp(col_name, "id") == 0) continue;
            
            if (!first) {
                strcat(columns, ", ");
                strcat(values, ", ");
            }
            strcat(columns, col_name);
            
            const char *entry_text = gtk_entry_get_text(GTK_ENTRY(entries[i-1]));
            strcat(values, "'");
            strcat(values, entry_text);
            strcat(values, "'");
            
            first = 0;
        }
        
        snprintf(sql, sizeof(sql), "INSERT INTO %s (%s) VALUES (%s)", 
                 data->table_name, columns, values);
        
        execute_sql(sql, &errmsg);
        refresh_table_view(data);
    }
    
    sqlite3_free_table(result);
    gtk_widget_destroy(dialog);
}

void on_delete_button_clicked(GtkButton *button, TableData *data) {
    GtkTreeSelection *selection;
    GtkTreeModel *model;
    GtkTreeIter iter;
    char sql[256];
    char *errmsg = NULL;
    
    selection = gtk_tree_view_get_selection(GTK_TREE_VIEW(data->treeview));
    if (gtk_tree_selection_get_selected(selection, &model, &iter)) {
        gchar *id;
        gtk_tree_model_get(model, &iter, 0, &id, -1);
        
        snprintf(sql, sizeof(sql), "DELETE FROM %s WHERE id = %s", data->table_name, id);
        execute_sql(sql, &errmsg);
        refresh_table_view(data);
        g_free(id);
    } else {
        gtk_label_set_text(GTK_LABEL(status_label), "Выберите запись для удаления");
    }
}

void on_refresh_button_clicked(GtkButton *button, TableData *data) {
    refresh_table_view(data);
    gtk_label_set_text(GTK_LABEL(status_label), "Таблица обновлена");
}

void create_table_tab(const char *table_name) {
    GtkWidget *vbox, *hbox, *scrolled_window, *treeview;
    GtkWidget *add_button, *delete_button, *refresh_button;
    GtkListStore *store;
    GtkCellRenderer *renderer;
    GtkTreeViewColumn *column;
    char **result;
    int rows, cols;
    char *errmsg = NULL;
    char sql[256];

    vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    hbox = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 5);
    scrolled_window = gtk_scrolled_window_new(NULL, NULL);

    snprintf(sql, sizeof(sql), "PRAGMA table_info(%s)", table_name);
    if (sqlite3_get_table(db, sql, &result, &rows, &cols, &errmsg) != SQLITE_OK) {
        gtk_label_set_text(GTK_LABEL(status_label), errmsg);
        sqlite3_free(errmsg);
        return;
    }

    GType types[rows];
    for (int i = 0; i < rows; i++) {
        types[i] = G_TYPE_STRING;
    }
    store = gtk_list_store_newv(rows, types);

    treeview = gtk_tree_view_new_with_model(GTK_TREE_MODEL(store));
    g_object_unref(store);

    for (int i = 1; i <= rows; i++) {
        renderer = gtk_cell_renderer_text_new();
        column = gtk_tree_view_column_new_with_attributes(
            result[i * cols + 1], renderer, "text", i-1, NULL);
        gtk_tree_view_append_column(GTK_TREE_VIEW(treeview), column);
    }

    add_button = gtk_button_new_with_label("Добавить");
    delete_button = gtk_button_new_with_label("Удалить");
    refresh_button = gtk_button_new_with_label("Обновить");

    gtk_container_add(GTK_CONTAINER(scrolled_window), treeview);
    gtk_box_pack_start(GTK_BOX(vbox), scrolled_window, TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(hbox), add_button, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(hbox), delete_button, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(hbox), refresh_button, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), hbox, FALSE, FALSE, 0);

    GtkWidget *label = gtk_label_new(table_name);
    gtk_notebook_append_page(GTK_NOTEBOOK(notebook), vbox, label);

    TableData *data = g_malloc(sizeof(TableData));
    data->treeview = treeview;
    data->store = store;
    data->table_name = g_strdup(table_name);

    g_signal_connect(add_button, "clicked", G_CALLBACK(on_add_button_clicked), data);
    g_signal_connect(delete_button, "clicked", G_CALLBACK(on_delete_button_clicked), data);
    g_signal_connect(refresh_button, "clicked", G_CALLBACK(on_refresh_button_clicked), data);

    refresh_table_view(data);
    
    sqlite3_free_table(result);
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "SQLite Database Wrapper");
    gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    GtkWidget *vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    notebook = gtk_notebook_new();
    status_label = gtk_label_new("Готово");

    if (sqlite3_open("company.db", &db) != SQLITE_OK) {
        gtk_label_set_text(GTK_LABEL(status_label), sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    char *errmsg = NULL;
    const char *create_tables_sql = 
        "CREATE TABLE IF NOT EXISTS Должность (id INTEGER PRIMARY KEY, Наименование TEXT);"
        "CREATE TABLE IF NOT EXISTS Организация (id INTEGER PRIMARY KEY, ИНН TEXT, Название TEXT);"
        "CREATE TABLE IF NOT EXISTS Сотрудник (id INTEGER PRIMARY KEY, ФИО TEXT, "
        "Дата_рождения TEXT, Пол TEXT);";
    
    execute_sql(create_tables_sql, &errmsg);

    create_table_tab("Должность");
    create_table_tab("Сотрудник");
    create_table_tab("Организация");

    gtk_box_pack_start(GTK_BOX(vbox), notebook, TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), status_label, FALSE, FALSE, 0);
    gtk_container_add(GTK_CONTAINER(window), vbox);

    gtk_widget_show_all(window);
    gtk_main();

    sqlite3_close(db);
    
    return 0;
}